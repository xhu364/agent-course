from state import State


def create_improve_node(llm):
    def improve(state: State):
        attempt = state["attempts"] + 1

        prompt = f"""
Answer the following question:

Question: {state["question"]}

This is attempt {attempt}.
"""

        response = llm.invoke(prompt)

        print(f"LLM response: {response.content}")
        return {"answer": [response.content], "attempts": attempt}

    return improve
