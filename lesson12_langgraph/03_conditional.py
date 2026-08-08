from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    question: str
    answer: str
    score: int


def generate(state: State):
    return {"answer": "Python is a programming language."}


def evaluate(state: State):
    if "Python" in state["answer"]:
        return {"score": 1}
    else:
        return {"score": 0}


def route(state):
    if state["score"] == 1:
        return "good"
    else:
        return "bad"


def improve(state: State):
    return {"answer": state["answer"] + " It is widely used in software development."}


graph = StateGraph(State)

graph.add_node("generate", generate)
graph.add_node("evaluate", evaluate)
graph.add_node("improve", improve)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")
graph.add_conditional_edges("evaluate", route, {"good": END, "bad": "improve"})

app = graph.compile()

result = app.invoke({})

print(result)
