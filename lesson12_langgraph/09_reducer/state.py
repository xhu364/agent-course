from typing import TypedDict, Annotated
import operator


class State(TypedDict):
    question: str
    answer: Annotated[list[str], operator.add]
    score: int
    attempts: int
    feedback: str
