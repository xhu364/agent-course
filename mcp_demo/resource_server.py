from mcp.server import MCPServer

mcp = MCPServer(
    "Resource Server",
)


@mcp.resource("config://server")
def server_config() -> str:
    """Return the server configuration."""
    return """
server_name: ubuntu-z640
environment: development
location: home-lab
port: 8002
"""


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8002)