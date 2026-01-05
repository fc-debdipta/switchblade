import os
import grpc
import json
import time
import importlib.util
import sys
import queue
import threading
import inspect  # <--- NEW: Needed to inspect module members
from concurrent import futures
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    from ..generated import switchblade_pb2
    from ..generated import switchblade_pb2_grpc
except ImportError:
    # When running directly, add parent directory to path
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
    from src.generated import switchblade_pb2
    from src.generated import switchblade_pb2_grpc

TOOLS_DIR = "./tools"


class ToolRegistry:
    def __init__(self):
        self.tools = {}  # Maps tool_name -> function_object (not module)
        self.subscribers = []
        self.lock = threading.Lock()

    def load_tool_file(self, filepath):
        """Dynamically loads a python module and scans for @tool decorated functions."""
        module_name = os.path.basename(filepath).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, filepath)

        if spec and spec.loader:
            try:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                # --- NEW LOGIC: SCAN FOR DECORATED FUNCTIONS ---
                loaded_count = 0
                for name, obj in inspect.getmembers(module):
                    # Check if it's a function and has our specific tag
                    if inspect.isfunction(obj) and getattr(
                        obj, "_is_switchblade_tool", False
                    ):
                        meta = obj._tool_metadata
                        tool_name = meta["name"]

                        with self.lock:
                            # Register the function object directly
                            self.tools[tool_name] = obj
                            print(
                                f"✅ Registered tool: {tool_name} (from {module_name})"
                            )
                            self.notify_subscribers(f"Tool '{tool_name}' updated")
                            loaded_count += 1

                if loaded_count == 0:
                    print(f"⚠️  No tools found in {module_name} (Did you forget @tool?)")

            except Exception as e:
                print(f"❌ Failed to load {module_name}: {e}")

    def notify_subscribers(self, message):
        active_subs = []
        for q in self.subscribers:
            try:
                q.put(
                    switchblade_pb2.ToolsNotification(
                        event_type="UPDATED", message=message
                    )
                )
                active_subs.append(q)
            except:
                pass
        self.subscribers = active_subs

    def register_subscriber(self, q):
        with self.lock:
            self.subscribers.append(q)

    def remove_subscriber(self, q):
        with self.lock:
            if q in self.subscribers:
                self.subscribers.remove(q)


class ToolFileHandler(FileSystemEventHandler):
    def __init__(self, registry):
        self.registry = registry

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.registry.load_tool_file(event.src_path)

    def on_created(self, event):
        if event.src_path.endswith(".py"):
            self.registry.load_tool_file(event.src_path)


class SwitchbladeServiceImpl(switchblade_pb2_grpc.SwitchbladeServiceServicer):
    def __init__(self, registry):
        self.registry = registry

    def ListTools(self, request, context):
        tool_list = []
        with self.registry.lock:
            for name, func_obj in self.registry.tools.items():
                # Extract metadata from the function object
                meta = func_obj._tool_metadata

                tool_list.append(
                    switchblade_pb2.Tool(
                        name=meta["name"],
                        description=meta["description"],
                        input_schema_json=json.dumps(meta["input_schema"]),
                        output_schema_json=json.dumps(meta["output_schema"]),
                    )
                )
        return switchblade_pb2.ListToolsResponse(tools=tool_list)

    def CallTool(self, request, context):
        # Retrieve the function directly
        tool_func = self.registry.tools.get(request.tool_name)

        if not tool_func:
            return switchblade_pb2.CallToolResponse(
                is_error=True, error_message=f"Tool '{request.tool_name}' not found"
            )

        try:
            args = json.loads(request.arguments_json) if request.arguments_json else {}

            # --- EXECUTE THE FUNCTION DIRECTLY ---
            result = tool_func(args)

            return switchblade_pb2.CallToolResponse(
                content_json=json.dumps(result), is_error=False
            )
        except Exception as e:
            return switchblade_pb2.CallToolResponse(is_error=True, error_message=str(e))

    def WatchTools(self, request, context):
        q = queue.Queue()
        self.registry.register_subscriber(q)
        try:
            while context.is_active():
                notification = q.get()
                yield notification
        except Exception:
            pass
        finally:
            self.registry.remove_subscriber(q)


def serve():
    registry = ToolRegistry()

    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR)

    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith(".py"):
            registry.load_tool_file(os.path.join(TOOLS_DIR, filename))

    observer = Observer()
    observer.schedule(ToolFileHandler(registry), path=TOOLS_DIR, recursive=False)
    observer.start()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    switchblade_pb2_grpc.add_SwitchbladeServiceServicer_to_server(
        SwitchbladeServiceImpl(registry), server
    )

    server.add_insecure_port("[::]:50051")
    print("🚀 Switchblade Server running on port 50051...")

    try:
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        observer.stop()
        server.stop(0)
    observer.join()


if __name__ == "__main__":
    serve()
