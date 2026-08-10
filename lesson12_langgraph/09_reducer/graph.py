from langgraph.graph import StateGraph, START, END
from state import State
from nodes import create_generate_node, create_improve_node, create_evaluate_node
from typing import Literal

PASS_SCORE = 1


class Conversation:
    def __init__(self, llm, max_attempts=5):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.llm = llm
        self.max_attempts = max_attempts
        self.app = self._build_graph()

    def _build_graph(self):
        # build graph
        generate = create_generate_node(self.llm)
        evaluate = create_evaluate_node(self.llm)
        improve = create_improve_node(self.llm)
        graph = StateGraph(State)
        graph.add_node("generate", generate)
        graph.add_node("evaluate", evaluate)
        graph.add_node("improve", improve)

        graph.add_edge(START, "generate")
        graph.add_edge("generate", "evaluate")
        graph.add_conditional_edges(
            "evaluate",
            self.route,
            {"good": END, "max_attempts_reached": END, "bad": "improve"},
        )
        graph.add_edge("improve", "evaluate")
        return graph.compile()

    def route(self, state: State) -> Literal["good", "bad", "max_attempts_reached"]:
        if state["score"] == PASS_SCORE:
            return "good"
        elif state["attempts"] >= self.max_attempts:
            return "max_attempts_reached"
        else:
            return "bad"


#                 ┌──────────────┐
#                 │   generate   │
#                 │     LLM      │
#                 └──────┬───────┘
#                        │
#                        │ attempts + 1
#                        ▼
#                 ┌──────────────┐
#                 │   evaluate   │
#                 │     LLM      │
#                 └──────┬───────┘
#                        │
#                 score + feedback
#                        │
#             ┌──────────┴──────────┐
#             │                     │
#          score=1              score=0
#             │                     │
#             ▼                     ▼
#            END                attempts?
#                                  │
#                           ┌──────┴──────┐
#                           │             │
#                          yes            no
#                           │             │
#                           ▼             ▼
#                          END          improve
#                                         │
#                                         │ attempts + 1
#                                         ▼
#                                     evaluate
#                                         │
#                                         └─── loop
