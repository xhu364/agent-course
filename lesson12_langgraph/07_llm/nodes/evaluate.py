from state import State


def evaluate(state: State):
    if "python" in state["answer"].lower() or state["attempts"] > 5:
        return {"score": 1, "feedback": "Good answer."}
    else:
        return {"score": 0, "feedback": "The answer should mention Python."}
