from mcp.server import MCPServer
import platform
import shutil

import psutil


mcp = MCPServer("demo-server")

@mcp.tool()
def add_integers(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Return the product of two integers."""
    return a * b


@mcp.tool()
def get_server_info() -> dict:
    """Return basic information about the server host."""
    return {
        "hostname": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "processor": platform.processor(),
    }


@mcp.tool()
def get_cpu_usage() -> float:
    """Return the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)


@mcp.tool()
def get_memory_usage() -> dict:
    """Return current memory usage statistics in bytes and percent."""
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "percent": memory.percent,
    }


@mcp.tool()
def get_disk_usage(path: str = "/") -> dict:
    """Return disk usage statistics for the specified path."""
    usage = shutil.disk_usage(path)
    percent = usage.used / usage.total * 100 if usage.total else 0.0
    return {
        "path": path,
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "percent": percent,
    }

@mcp.resource("config://server")
def server_config() -> str:
    """Return the server configuration."""
    return """
server_name: ubuntu-z640
environment: development
location: home-lab
port: 8002
"""

@mcp.resource("document://employee-handbook")
def employee_handbook():
    return """
    Employees receive 20 days of PTO...
    """

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)