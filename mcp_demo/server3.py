from mcp.server import MCPServer

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
def get_server_info() -> str:
    """Return information about the server."""
    return f"Server Name: {mcp.name}, Number of Tools: "

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)