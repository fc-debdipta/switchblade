"""
MCP Server Implementation
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServer:
    """
    Model Context Protocol Server
    
    A flexible server implementation for handling MCP protocol requests,
    managing context, and executing registered tools/functions.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        """
        Initialize the MCP Server
        
        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.tools: Dict[str, Callable] = {}
        self.context: Dict[str, Any] = {}
        self.server = None
        
    def register_tool(self, name: str, func: Callable, description: str = ""):
        """
        Register a tool/function that can be called by clients
        
        Args:
            name: Tool name
            func: Callable function
            description: Tool description
        """
        self.tools[name] = {
            "function": func,
            "description": description
        }
        logger.info(f"Registered tool: {name}")
        
    def update_context(self, key: str, value: Any):
        """
        Update server context
        
        Args:
            key: Context key
            value: Context value
        """
        self.context[key] = value
        logger.info(f"Updated context: {key}")
        
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Handle individual client connections
        
        Args:
            reader: Stream reader
            writer: Stream writer
        """
        addr = writer.get_extra_info('peername')
        logger.info(f"Client connected: {addr}")
        
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                    
                message = json.loads(data.decode())
                logger.info(f"Received request: {message.get('type', 'unknown')}")
                
                response = await self.process_request(message)
                
                writer.write(json.dumps(response).encode())
                await writer.drain()
                
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            logger.info(f"Client disconnected: {addr}")
            writer.close()
            await writer.wait_closed()
            
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming requests
        
        Args:
            request: Request dictionary
            
        Returns:
            Response dictionary
        """
        request_type = request.get("type")
        
        if request_type == "ping":
            return {"status": "success", "message": "pong", "timestamp": datetime.utcnow().isoformat()}
            
        elif request_type == "list_tools":
            tools_list = {
                name: {"description": tool["description"]}
                for name, tool in self.tools.items()
            }
            return {"status": "success", "tools": tools_list}
            
        elif request_type == "call_tool":
            tool_name = request.get("tool")
            args = request.get("args", {})
            
            if tool_name not in self.tools:
                return {"status": "error", "message": f"Tool '{tool_name}' not found"}
                
            try:
                result = await self._execute_tool(tool_name, args)
                return {"status": "success", "result": result}
            except Exception as e:
                return {"status": "error", "message": str(e)}
                
        elif request_type == "get_context":
            return {"status": "success", "context": self.context}
            
        else:
            return {"status": "error", "message": f"Unknown request type: {request_type}"}
            
    async def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """
        Execute a registered tool
        
        Args:
            tool_name: Name of the tool to execute
            args: Arguments for the tool
            
        Returns:
            Tool execution result
        """
        func = self.tools[tool_name]["function"]
        
        if asyncio.iscoroutinefunction(func):
            return await func(**args)
        else:
            return func(**args)
            
    async def start(self):
        """Start the MCP server"""
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        
        addr = self.server.sockets[0].getsockname()
        logger.info(f"MCP Server started on {addr}")
        
        async with self.server:
            await self.server.serve_forever()
            
    async def stop(self):
        """Stop the MCP server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("MCP Server stopped")


async def main():
    """Main entry point for running the server"""
    server = MCPServer()
    
    # Example tool registration
    def example_tool(text: str) -> str:
        return f"Processed: {text}"
    
    server.register_tool("example", example_tool, "An example tool")
    
    try:
        await server.start()
    except KeyboardInterrupt:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
