CODE_REVIEW_TEMPLATE = """
You are a senior software engineer.

Review this code:

{code}

Find:
- bugs
- security issues
- performance issues

Provide suggestions.
"""


def create_prompt(code):
    return CODE_REVIEW_TEMPLATE.format(
        code=code
    )