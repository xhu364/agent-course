import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from requests import session


async def main():
    url = "http://127.0.0.1:8000/mcp"

    async with streamable_http_client(url) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")
                print(f"  {tool.description}")

            result = await session.call_tool(
                "get_cpu_usage",
                arguments={},
            )

            print("Result:")
            print(result)

            result = await session.call_tool(
                "get_memory_usage",
                arguments={},
            )

            print("Result:")
            print(result)

            result = await session.call_tool(
                "get_disk_usage",
                arguments={
                    "path": "/",
                },
            )

            print("Result:")
            print(result)




if __name__ == "__main__":
    asyncio.run(main())