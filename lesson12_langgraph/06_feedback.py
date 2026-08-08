from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    question: str
    answer: str
    score: int
    attempts: int
    feedback: str


def generate(state: State):
    attempt = state["attempts"] + 1

    if attempt == 1:
        answer = "It is a programming language."
    else:
        answer = "It is a Python programming language."

    return {"answer": answer, "attempts": attempt}


def evaluate(state: State):
    if "python" in state["answer"].lower() or state["attempts"] > 5:
        return {"score": 1, "feedback": "Good answer."}
    else:
        return {"score": 0, "feedback": "The answer should mention Python."}


def improve(state: State):
    return {"answer": "It is a Python programming language."}


def route(state: State):
    if state["score"] == 1:
        return "good"
    else:
        return "bad"


graph = StateGraph(State)
graph.add_node("generate", generate)
graph.add_node("evaluate", evaluate)
graph.add_node("improve", improve)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")
graph.add_conditional_edges("evaluate", route, {"good": END, "bad": "improve"})
graph.add_edge("improve", "generate")

app = graph.compile()

result = app.invoke({"attempts": 0, "score": 0})
print(result)
