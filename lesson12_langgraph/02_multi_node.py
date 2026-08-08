from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    greeting: str
    final: str


def generate(state: State):
    return {"greeting": f"hello {state['name']}"}


def uppercase(state: State):
    return {"final": state["greeting"].upper()}


graph = StateGraph(State)

graph.add_node("generate", generate)
graph.add_node("uppercase", uppercase)

graph.add_edge(START, "generate")
graph.add_edge("generate", "uppercase")
graph.add_edge("uppercase", END)

app = graph.compile()

result = app.invoke({"name": "Mike"})

print(result)
