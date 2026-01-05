"""
MCP Client Implementation
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPClient:
    """
    Model Context Protocol Client
    
    A client implementation for connecting to MCP servers and executing
    remote tool calls.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        """
        Initialize the MCP Client
        
        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.connected = False
        
    async def connect(self):
        """Connect to the MCP server"""
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port
            )
            self.connected = True
            logger.info(f"Connected to MCP server at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
            
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.connected = False
            logger.info("Disconnected from MCP server")
            
    async def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a request to the server
        
        Args:
            request: Request dictionary
            
        Returns:
            Response dictionary
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")
            
        try:
            # Send request
            self.writer.write(json.dumps(request).encode())
            await self.writer.drain()
            
            # Receive response
            data = await self.reader.read(4096)
            response = json.loads(data.decode())
            
            return response
        except Exception as e:
            logger.error(f"Error sending request: {e}")
            raise
            
    async def ping(self) -> Dict[str, Any]:
        """
        Send a ping request to the server
        
        Returns:
            Server response
        """
        return await self.send_request({"type": "ping"})
        
    async def list_tools(self) -> Dict[str, Any]:
        """
        List available tools on the server
        
        Returns:
            Dictionary of available tools
        """
        return await self.send_request({"type": "list_tools"})
        
    async def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a tool on the server
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Tool execution result
        """
        request = {
            "type": "call_tool",
            "tool": tool_name,
            "args": kwargs
        }
        return await self.send_request(request)
        
    async def get_context(self) -> Dict[str, Any]:
        """
        Get the current context from the server
        
        Returns:
            Server context
        """
        return await self.send_request({"type": "get_context"})
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()


async def main():
    """Main entry point for testing the client"""
    async with MCPClient() as client:
        # Test ping
        response = await client.ping()
        logger.info(f"Ping response: {response}")
        
        # List tools
        tools = await client.list_tools()
        logger.info(f"Available tools: {tools}")
        
        # Call a tool
        result = await client.call_tool("example", text="Hello, MCP!")
        logger.info(f"Tool result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
