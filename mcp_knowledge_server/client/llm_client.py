import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

from .llm import create_llm


async def main():

    # ----------------------------------
    # 1. MCP client
    # ----------------------------------

    client = MultiServerMCPClient(
        {
            "knowledge": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "http",
            }
        }
    )

    # ----------------------------------
    # 2. Get MCP tools
    # ----------------------------------

    tools = await client.get_tools()

    print("Available MCP tools:")

    for tool in tools:
        print(f"- {tool.name}")
        print(f"  {tool.description}")

    # ----------------------------------
    # 3. Create Gemini
    # ----------------------------------

    model = create_llm("gemini")

    # ----------------------------------
    # 4. Create agent
    # ----------------------------------

    agent = create_agent(
        model=model,
        tools=tools,
    )

    # ----------------------------------
    # 5. Ask Gemini
    # ----------------------------------

    result = await agent.ainvoke(
        {
            "messages": [
                ("user", "How many vacation days do " "full-time employees receive?")
            ]
        }
    )

    # ----------------------------------
    # 6. Print messages
    # ----------------------------------

    for message in result["messages"]:

        print("\n--------------------")

        print(type(message).__name__)

        print("Content:")
        print(message.content)

        if hasattr(message, "tool_calls"):
            if message.tool_calls:
                print("Tool calls:")
                print(message.tool_calls)


if __name__ == "__main__":
    asyncio.run(main())
