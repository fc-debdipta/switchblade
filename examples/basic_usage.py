"""
Example usage of Switchblade MCP Server and Client
"""

import asyncio
from src.server import MCPServer
from src.client import MCPClient


def greet(name: str, greeting: str = "Hello") -> str:
    """Example tool: Greet someone"""
    return f"{greeting}, {name}!"


def calculate(operation: str, a: float, b: float) -> float:
    """Example tool: Perform basic calculations"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf')
    }
    return operations.get(operation, lambda x, y: 0)(a, b)


async def run_server():
    """Run the MCP server with example tools"""
    server = MCPServer(host="localhost", port=8765)
    
    # Register tools
    server.register_tool("greet", greet, "Greet someone with a custom message")
    server.register_tool("calculate", calculate, "Perform basic arithmetic operations")
    
    # Update context
    server.update_context("version", "1.0.0")
    server.update_context("server_name", "Switchblade MCP Server")
    
    print("Starting MCP Server...")
    await server.start()


async def run_client():
    """Run the MCP client and test server tools"""
    await asyncio.sleep(2)  # Wait for server to start
    
    async with MCPClient(host="localhost", port=8765) as client:
        print("\n=== Testing MCP Client ===\n")
        
        # Test ping
        response = await client.ping()
        print(f"Ping: {response}")
        
        # List available tools
        tools = await client.list_tools()
        print(f"\nAvailable tools: {tools}")
        
        # Get context
        context = await client.get_context()
        print(f"\nServer context: {context}")
        
        # Call greet tool
        result = await client.call_tool("greet", name="Switchblade", greeting="Welcome")
        print(f"\nGreet result: {result}")
        
        # Call calculate tool
        result = await client.call_tool("calculate", operation="add", a=10, b=5)
        print(f"\nCalculate result: {result}")


async def main():
    """Main entry point"""
    # Run server and client concurrently
    await asyncio.gather(
        run_server(),
        run_client()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nShutting down...")
