from typing import TypedDict

import os
import sys
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver

# Ensure project root is importable when running the script directly.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

from agents.agent import SingleAgent

# Use LangChain chat-model adapters
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


class State(TypedDict):
	user_request: str
	agent1: str
	agent2: str
	agent3: str
	summary: str


def build_model():
	llm_type = os.environ.get("LLM_TYPE", "ollama").lower()
	if llm_type == "ollama":
		return ChatOllama(model="llama3.2:3b", temperature=0.0)
	if llm_type == "gemini":
		return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.0)
	# Default fallback
	return ChatOllama(model="llama3.2:3b", temperature=0.0)


def router_node(state: State) -> dict:
	"""LLM-based router: returns a small key 'selected' with value 'agent1' or 'agent3'.

	The router uses a chat-model adapter via `SingleAgent` and is instructed to
	output exactly one word: either `agent1` or `agent3`.
	"""
	llm = build_model()
	agent = SingleAgent(
		llm=llm,
		system_prompt=(
			"You are the router. Given a user's request, choose exactly one of: 'agent1' or 'agent3'. "
			"Respond with only the chosen token (agent1 or agent3) and nothing else."
		),
		max_iterations=1,
	)

	output = agent.run(state["user_request"]).strip().lower()
	if "agent3" in output:
		selected = "agent3"
	else:
		selected = "agent1"

	# Store selection in the state under a transient key 'selected'.
	return {"selected": selected}


def agent1_node(state: State) -> dict:
	agent = SingleAgent(llm=build_model(), system_prompt="You are agent1.", max_iterations=3)
	return {"agent1": agent.run(state["user_request"]) }


def agent3_node(state: State) -> dict:
	agent = SingleAgent(llm=build_model(), system_prompt="You are agent3.", max_iterations=3)
	return {"agent3": agent.run(state["user_request"]) }


def agent2_node(state: State) -> dict:
	# agent2 must receive only the selected agent's output.
	selected = state.get("selected")
	if selected not in ("agent1", "agent3"):
		raise RuntimeError("Router did not select a valid agent for agent2 input.")

	selected_output = state.get(selected, "")
	agent = SingleAgent(llm=build_model(), system_prompt="You are agent2. Refine the selected agent's output.", max_iterations=3)
	return {"agent2": agent.run(selected_output) }


def summary_agent_node(state: State) -> dict:
	# summary_agent receives only agent2 output and produces final response.
	agent = SingleAgent(llm=build_model(), system_prompt="You are the summary agent. Produce the final response from agent2 output only.", max_iterations=3)
	return {"summary": agent.run(state["agent2"]) }


def build_graph() -> StateGraph:
	graph = StateGraph(State)

	graph.add_node("router", router_node)
	graph.add_node("agent1", agent1_node)
	graph.add_node("agent3", agent3_node)
	graph.add_node("agent2", agent2_node)
	graph.add_node("summary_agent", summary_agent_node)

	# Start with the router
	graph.add_edge(START, "router")

	# Router conditional edges pick exactly one agent to act as the selected agent
	graph.add_edge("router", "agent1", condition=lambda s: s.get("selected") == "agent1")
	graph.add_edge("router", "agent3", condition=lambda s: s.get("selected") == "agent3")

	# Selected agent -> agent2 -> summary_agent
	graph.add_edge("agent1", "agent2")
	graph.add_edge("agent3", "agent2")
	graph.add_edge("agent2", "summary_agent")

	return graph.compile(checkpointer=MemorySaver())


def main() -> None:
	app = build_graph()

	initial_state: State = {
		"user_request": "Please explain alpha workflows and when to use them.",
		"agent1": "",
		"agent2": "",
		"agent3": "",
		"summary": "",
	}

	result = app.invoke(initial_state, config={"configurable": {"thread_id": "demo-llm-router"}})
	print("Final summary:\n")
	print(result["summary"])


if __name__ == "__main__":
	main()

