from typing import TypedDict
from langgraph.graph import START, END, StateGraph


class State(TypedDict):
    name: str
    greeting: str


def hello(state: State):
    return {"greeting": f"hi {state['name']}"}


graph = StateGraph(State)

graph.add_node("hello", hello)
graph.add_edge(START, "hello")
graph.add_edge("hello", END)

app = graph.compile()

result = app.invoke({"name": "Matt"})
print(result)
