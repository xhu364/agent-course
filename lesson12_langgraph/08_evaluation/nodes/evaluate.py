from state import State
import json


def create_evaluate_node(llm):
    def evaluate(state: State):
        prompt = f"""
Evaluate the following answer to the question:

Question: {state["question"]}

Answer: {state["answer"]}

Provide a score from 0 to 1 and feedback. If the answer is correct, give a score of 1 and
feedback "Good answer." If the answer is incorrect, give a score of 0 and feedback
"The answer should compare with other languages."

The answer should not contain any text outside of json and shouldbe in the following JSON format:
{{
    "score": <score>,
    "feedback": "<feedback>"
}}
"""
        response = llm.invoke(prompt)
        print(f"myprompt: {prompt}")
        print(f"myresponse: {response.content}")
        result = json.loads(response.content)
        return {
            "score": result["score"],
            "feedback": result["feedback"],
        }

    return evaluate
