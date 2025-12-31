"""
Tests for MCP Server
"""

import pytest
import asyncio
from src.server import MCPServer


@pytest.fixture
async def server():
    """Fixture to create a test server"""
    srv = MCPServer(host="localhost", port=8766)
    yield srv
    await srv.stop()


def test_server_initialization():
    """Test server initialization"""
    server = MCPServer()
    assert server.host == "localhost"
    assert server.port == 8765
    assert len(server.tools) == 0


def test_register_tool():
    """Test tool registration"""
    server = MCPServer()
    
    def dummy_tool():
        return "test"
    
    server.register_tool("dummy", dummy_tool, "A dummy tool")
    assert "dummy" in server.tools
    assert server.tools["dummy"]["description"] == "A dummy tool"


def test_update_context():
    """Test context updates"""
    server = MCPServer()
    server.update_context("key1", "value1")
    assert server.context["key1"] == "value1"


@pytest.mark.asyncio
async def test_process_ping_request():
    """Test ping request processing"""
    server = MCPServer()
    request = {"type": "ping"}
    response = await server.process_request(request)
    assert response["status"] == "success"
    assert response["message"] == "pong"


@pytest.mark.asyncio
async def test_process_list_tools_request():
    """Test list tools request"""
    server = MCPServer()
    
    def tool1():
        pass
    
    server.register_tool("tool1", tool1, "Tool 1")
    
    request = {"type": "list_tools"}
    response = await server.process_request(request)
    assert response["status"] == "success"
    assert "tool1" in response["tools"]


@pytest.mark.asyncio
async def test_process_call_tool_request():
    """Test tool call request"""
    server = MCPServer()
    
    def add(a, b):
        return a + b
    
    server.register_tool("add", add, "Addition tool")
    
    request = {"type": "call_tool", "tool": "add", "args": {"a": 5, "b": 3}}
    response = await server.process_request(request)
    assert response["status"] == "success"
    assert response["result"] == 8
