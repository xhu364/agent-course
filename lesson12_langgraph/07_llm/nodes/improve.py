from state import State


def improve(state: State):
    return {
        "question": state["question"] + state["feedback"],
    }
