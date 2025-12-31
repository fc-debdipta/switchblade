"""
Tests for MCP Client
"""

import pytest
import asyncio
from src.client import MCPClient


def test_client_initialization():
    """Test client initialization"""
    client = MCPClient()
    assert client.host == "localhost"
    assert client.port == 8765
    assert client.connected is False


def test_client_custom_params():
    """Test client with custom parameters"""
    client = MCPClient(host="192.168.1.1", port=9000)
    assert client.host == "192.168.1.1"
    assert client.port == 9000


@pytest.mark.asyncio
async def test_client_connection_error():
    """Test client connection error handling"""
    client = MCPClient(host="localhost", port=9999)
    
    with pytest.raises(Exception):
        await client.connect()


@pytest.mark.asyncio
async def test_send_request_without_connection():
    """Test sending request without connection"""
    client = MCPClient()
    
    with pytest.raises(ConnectionError):
        await client.send_request({"type": "ping"})
