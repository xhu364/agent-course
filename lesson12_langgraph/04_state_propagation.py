from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    question: str
    answer: str
    score: int
    result: str


def generate(state: State):
    return {"answer": "Python is a programming language"}


def add_score(state: State):
    if "Python" in state["answer"]:
        return {"score": 1}
    else:
        return {"score": 0}


def format_result(state: State):
    return {"result": f'answer {state["answer"]} and score {state["score"]}'}


graph = StateGraph(State)
graph.add_node("generate", generate)
graph.add_node("add_score", add_score)
graph.add_node("format_result", format_result)

graph.add_edge(START, "generate")
graph.add_edge("generate", "add_score")
graph.add_edge("add_score", "format_result")
graph.add_edge("format_result", END)

app = graph.compile()

result = app.invoke({"question": "What is Python"})
print(result)
