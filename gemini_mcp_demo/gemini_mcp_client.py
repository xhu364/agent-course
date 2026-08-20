import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from llm import create_llm


async def main():

    # ----------------------------------
    # 1. Connect to MCP server
    # ----------------------------------

    client = MultiServerMCPClient(
        {
            "math": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "http",
            }
        }
    )

    # ----------------------------------
    # 2. Load MCP tools
    # ----------------------------------

    tools = await client.get_tools()

    print("Loaded MCP tools:")

    for tool in tools:
        print(f"  - {tool.name}")

    # ----------------------------------
    # 3. Create LLM
    # ----------------------------------

    model = create_llm("gemini")

    # ----------------------------------
    # 4. Create ReAct agent
    # ----------------------------------

    agent = create_agent(
        model=model,
        tools=tools,
    )

    # ----------------------------------
    # 5. Ask question
    # ----------------------------------

    result = await agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    "How much memory in MB is currently being used?",
                )
            ]
        }
    )

    # ----------------------------------
    # 6. Print final answer
    # ----------------------------------

    print(result["messages"])
    for message in result["messages"]:
        print("\n---")
        print("Type:", type(message).__name__)
        print("Content:", message.content)

        if hasattr(message, "tool_calls"):
            print("Tool calls:", message.tool_calls)
    #print("\nFinal answer:")
    #print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())

