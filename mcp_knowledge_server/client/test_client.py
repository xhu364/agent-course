import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


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
                "search_documents",
                arguments={
                    "query": "How many vacation days do full-time employees receive?",
                    "top_k": 3,
                },
            )

            print("\nSearch result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())