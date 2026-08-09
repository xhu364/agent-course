from state import State


def create_generate_node(llm):
    def generate(state: State):
        attempt = state["attempts"] + 1

        response = llm.invoke(f"""
Answer the following question:

Question: {state["question"]}

This is attempt {attempt}.
            """)

        return {"answer": response.content, "attempts": attempt}

    return generate
