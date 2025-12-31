# 🗡️ Switchblade

> A lightning-fast, flexible Python implementation of the Model Context Protocol (MCP) server and client architecture.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📖 Overview

**Switchblade** is a custom implementation of the Model Context Protocol (MCP) that provides a robust, asynchronous server-client architecture for managing AI model contexts, executing remote tools, and facilitating seamless communication between AI systems and external services.

The name "Switchblade" reflects the project's core design philosophy: **quick to deploy, sharp in execution, and compact in design** - much like its namesake.

## ✨ Features

- 🚀 **Asynchronous Architecture**: Built on Python's `asyncio` for high-performance concurrent operations
- 🔧 **Dynamic Tool Registration**: Easily register and expose custom tools/functions to clients
- 📡 **Context Management**: Maintain and share state across multiple client connections
- 🔌 **Simple Protocol**: JSON-based communication protocol for easy integration
- 🧪 **Well-Tested**: Comprehensive test suite using pytest
- 📦 **Modular Design**: Clean separation between server and client components
- 🎯 **Type-Safe**: Fully typed codebase for better IDE support and fewer runtime errors

## 🏗️ Architecture

```
┌─────────────────┐         JSON/TCP          ┌─────────────────┐
│                 │ ◄────────────────────────► │                 │
│   MCP Client    │                            │   MCP Server    │
│                 │  - ping                    │                 │
│  - connect()    │  - list_tools              │  - register()   │
│  - call_tool()  │  - call_tool               │  - execute()    │
│  - disconnect() │  - get_context             │  - context      │
└─────────────────┘                            └─────────────────┘
```

### Core Components

1. **MCPServer**: Manages incoming connections, executes registered tools, and maintains shared context
2. **MCPClient**: Connects to MCP servers and provides a clean API for remote tool execution
3. **Protocol Layer**: JSON-based message format for requests and responses

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone git@github.com:fc-debdipta/switchblade.git
cd switchblade

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Basic Usage

#### Starting a Server

```python
import asyncio
from src.server import MCPServer

async def main():
    server = MCPServer(host="localhost", port=8765)
    
    # Register a custom tool
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    server.register_tool("greet", greet, "Greet someone")
    
    # Start the server
    await server.start()

asyncio.run(main())
```

#### Using a Client

```python
import asyncio
from src.client import MCPClient

async def main():
    async with MCPClient(host="localhost", port=8765) as client:
        # Ping the server
        response = await client.ping()
        print(response)
        
        # List available tools
        tools = await client.list_tools()
        print(tools)
        
        # Call a tool
        result = await client.call_tool("greet", name="World")
        print(result)

asyncio.run(main())
```

### Running Examples

```bash
# Run the basic usage example
python examples/basic_usage.py
```

## 📋 Protocol Specification

### Request Types

#### Ping
```json
{
  "type": "ping"
}
```

#### List Tools
```json
{
  "type": "list_tools"
}
```

#### Call Tool
```json
{
  "type": "call_tool",
  "tool": "tool_name",
  "args": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

#### Get Context
```json
{
  "type": "get_context"
}
```

### Response Format

```json
{
  "status": "success|error",
  "message": "Optional message",
  "result": "Tool execution result (for call_tool)",
  "tools": "Available tools (for list_tools)",
  "context": "Server context (for get_context)",
  "timestamp": "ISO 8601 timestamp (for ping)"
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_server.py -v
```

## 📁 Project Structure

```
switchblade/
├── src/
│   ├── __init__.py
│   ├── server/
│   │   ├── __init__.py
│   │   └── mcp_server.py
│   └── client/
│       ├── __init__.py
│       └── mcp_client.py
├── examples/
│   └── basic_usage.py
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   └── test_client.py
├── requirements.txt
├── setup.py
├── README.md
└── LICENSE
```

## 🛠️ Development

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setting Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov
```

### Code Style

This project follows PEP 8 guidelines and uses type hints throughout the codebase.

```bash
# Format code (optional)
black src/ tests/ examples/

# Type checking (optional)
mypy src/
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Use Cases

- **AI Model Orchestration**: Coordinate multiple AI models with shared context
- **Remote Function Execution**: Execute Python functions from remote clients
- **Microservices Communication**: Lightweight RPC mechanism for microservices
- **AI Agent Tools**: Provide tools and capabilities to AI agents
- **Distributed Computing**: Share computational tasks across network

## 🔮 Roadmap

- [ ] Add authentication and authorization
- [ ] Implement WebSocket support
- [ ] Add encryption for secure communication
- [ ] Create CLI tool for server management
- [ ] Add metrics and monitoring
- [ ] Support for streaming responses
- [ ] Plugin system for easy extensibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**fc-debdipta**

- GitHub: [@fc-debdipta](https://github.com/fc-debdipta)

## 🙏 Acknowledgments

- Inspired by the Model Context Protocol specification
- Built with Python's excellent asyncio library

## 📞 Support

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ and Python**
