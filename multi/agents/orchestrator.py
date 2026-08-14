from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import tool

from .single_agent import SingleAgent
from .research_agent import ResearchAgent
from .data_agent import DataAgent
from .writer_agent import WriterAgent


class Orchestrator:

    def __init__(self, llm: BaseChatModel):
        self.llm = llm

        self.research_agent = ResearchAgent(llm)
        self.data_agent = DataAgent(llm)
        self.writer_agent = WriterAgent(llm)

        self._create_agent_tools()

        self.agent = SingleAgent(
            llm=llm,
            tools=[
                self.research_tool,
                self.data_tool,
                self.writer_tool,
            ],
            system_prompt="""
You are the orchestrator of a multi-agent system.

Your job is to coordinate specialist agents.

Available specialists:

1. research_agent
   - Researches questions
   - Finds relevant facts
   - Separates facts from assumptions

2. data_agent
   - Performs numerical/data analysis
   - Identifies trends
   - Performs calculations

3. writer_agent
   - Converts findings into a clear final response

You should:

1. Understand the user's request.
2. Decide which specialist agents are needed.
3. Call the appropriate specialists.
4. Give specialists enough context.
5. Combine their results.
6. Call the writer when a polished response is needed.
7. Return the final answer.

Do not invent information.

For simple questions, you may answer directly.
For complex questions, delegate work to the appropriate specialists.
""",
            max_iterations=8,
        )

    def _create_agent_tools(self):

        @tool
        def research_tool(query: str) -> str:
            """
            Delegate a research task to the research specialist.
            """
            return self.research_agent.run(query)

        @tool
        def data_tool(query: str) -> str:
            """
            Delegate a data-analysis task to the data specialist.
            """
            return self.data_agent.run(query)

        @tool
        def writer_tool(context: str) -> str:
            """
            Ask the writing specialist to create the final response
            from the supplied context.
            """
            return self.writer_agent.run(context)

        self.research_tool = research_tool
        self.data_tool = data_tool
        self.writer_tool = writer_tool

    def run(self, user_query: str) -> str:
        return self.agent.run(user_query)
