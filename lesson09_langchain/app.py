from config import GEMINI_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GEMINI_API_KEY,
)
llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
)


translation_prompt = PromptTemplate.from_template("""
Translate the following sentence into {language}.

Sentence:
{sentence}
""")
## -----------------------------------------------------
## Inspect PromptTemplate
## -----------------------------------------------------
#
# print("=" * 80)
# print("PromptTemplate")
# print("=" * 80)
#
# print(translation_prompt)
# print()
#
## -----------------------------------------------------
## Invoke PromptTemplate ONLY
## -----------------------------------------------------
#
# prompt_value = translation_prompt.invoke(
#    {
#        "language": "French",
#        "sentence": "Good morning",
#    }
# )
#
# print("=" * 80)
# print("PromptValue")
# print("=" * 80)
#
# print(type(prompt_value))
# print()
#
# print(prompt_value)
# print()
#
# print(prompt_value.to_string())
# print()
#
## -----------------------------------------------------
## Send PromptValue to Gemini
## -----------------------------------------------------
#
# response = llm.invoke(prompt_value)
#
# print("=" * 80)
# print("LLM Response")
# print("=" * 80)
#
# print(type(response))
# print()
#
# print(response.content)
# print()
#
# print(response.usage_metadata)
# print()

# -----------------------------------------------------
# LCEL
# -----------------------------------------------------

chain = translation_prompt | llm

print("=" * 80)
print("LCEL")
print("=" * 80)

languages = [
    "French",
    "Japanese",
    "Spanish",
    "German",
]

# for language in languages:
#
#    response = chain.invoke(
#        {
#            "language": language,
#            "sentence": "Good morning",
#        }
#    )
#
#    print(f"{language:10} -> {response.content}")
#
# print()

explainer_prompt = PromptTemplate.from_template("""
Explain {topic} to a {level}.

Maximum {words} words.
""")

explainer_chain = explainer_prompt | llm

response = explainer_chain.invoke(
    {"topic": "Python decorator", "level": "advanced", "words": 200}
)
print(response.content)
