from langchain_core.prompts import ChatPromptTemplate

initial_prompt = ChatPromptTemplate.from_template("""
    Explain the following programming topic.

    Topic:
    {topic}
    """)

example_prompt = ChatPromptTemplate.from_template("""
    Explain the following programming topic.

    Topic:
    {explanation}

    Provide a few examples.
    """)


# Prompt 2: Interview questions
quiz_prompt = ChatPromptTemplate.from_template("""
    Create three interview questions about:

    {explanation}

    Include answers.
    """)


# Prompt 3: Keywords
keyword_prompt = ChatPromptTemplate.from_template("""
    Extract five important keywords about:

    {explanation}

    Return only a comma-separated list.
    """)