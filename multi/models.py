from langchain_core.language_models import BaseChatModel


def create_model(
    provider: str,
    model_name: str,
    **kwargs,
) -> BaseChatModel:

    provider = provider.lower()

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=model_name,
            **kwargs,
        )

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=model_name,
            **kwargs,
        )

    raise ValueError(
        f"Unsupported provider: {provider}"
    )
