"""A minimal MCP server exposing a greeting tool."""

from mcp.server import MCPServer


mcp = MCPServer("demo-server")


@mcp.tool()
def add(a: int, b: int) -> int:
	"""Return the sum of two integers."""
	return a + b

@mcp.tool()
def greet(name: str) -> str:
	"""Return a friendly greeting."""
	return f"Hello, {name}!"


if __name__ == "__main__":
	mcp.run()
