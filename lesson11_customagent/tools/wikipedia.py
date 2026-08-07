from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from datetime import datetime
from zoneinfo import ZoneInfo


def get_wikipedia_tool():
    """
    Returns a LangChain Wikipedia Tool.
    """

    wikipedia = WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=1000,
    )

    return WikipediaQueryRun(api_wrapper=wikipedia)
