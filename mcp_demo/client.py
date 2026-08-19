import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        #command="python",
        #args=["server2.py"],
        command="/home/xhuang/llm-agent-course/.venv/bin/python",
        args=["/home/xhuang/llm-agent-course/mcp_demo/server2.py"],

    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")
                print(f"  {tool.description}")

            result = await session.call_tool(
                "multiply",
                arguments={
                    "a": 5,
                    "b": 3,
                }
            )

            print("Result:")
            print(result)
            result = await session.call_tool(
                "get_server_info",
                arguments={
                },
            )

            print("Result:")
            print(result)
            result = await session.call_tool(
                "add_integers",
                arguments={
                    "a": 10,
                    "b": 20,
                },
            )

            print("Result:")
            print(result)

if __name__ == "__main__":
    asyncio.run(main())