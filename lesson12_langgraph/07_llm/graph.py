from langgraph.graph import StateGraph, START, END
from state import State
from nodes import create_generate_node, evaluate, improve


class Conversation:
    def __init__(self, llm):
        self.llm = llm
        self._app = self._build_graph()

    def _build_graph(self):
        # build graph
        generate = create_generate_node(self.llm)
        graph = StateGraph(State)
        graph.add_node("generate", generate)
        graph.add_node("evaluate", evaluate)
        graph.add_node("improve", improve)

        graph.add_edge(START, "generate")
        graph.add_edge("generate", "evaluate")
        graph.add_conditional_edges(
            "evaluate", self.route, {"good": END, "bad": "improve"}
        )
        graph.add_edge("improve", "generate")
        return graph.compile()

    def route(self, state: State):
        if state["score"] == 1:
            return "good"
        else:
            return "bad"

    @property
    def app(self):
        return self._app
