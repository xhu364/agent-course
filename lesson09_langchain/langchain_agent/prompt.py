from langchain_core.prompts import ChatPromptTemplate

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant.
            Use tools when necessary.
            """,
        ),
        ("human", "{input}"),
    ]
)
