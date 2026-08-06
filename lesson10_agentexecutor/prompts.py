from langchain_core.prompts import ChatPromptTemplate


def get_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful assistant.

        You have access to several tools.
        Use them whenever they are helpful.

        If the user's request is missing information required to use a tool,
        ask a follow-up question instead of guessing.

        Do not make up weather, time, or Wikipedia facts.
        """,
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
