from typing import TypedDict


class State(TypedDict):
    question: str
    answer: str
    score: int
    attempts: int
    feedback: str
