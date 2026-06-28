# app/services/llm_service.py
from groq import Groq
from app.core.config import get_settings

settings = get_settings()


def get_groq_client() -> Groq:
    """
    Returns a Groq client instance.
    The API key is automatically read from settings.
    """
    return Groq(api_key=settings.groq_api_key)


def ask_llm(
    prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    temperature: float = 0.1,
    max_tokens: int = 1000,
) -> str:
    """
    Sends a prompt to the Groq LLM and returns the text response.

    Args:
        prompt: The user's message
        system_prompt: Instructions that define the model's behavior
        temperature: 0.0 = deterministic, 1.0 = creative. We use 0.1
                     for structured outputs to keep responses consistent.
        max_tokens: Maximum length of the response

    Returns:
        The model's response as a plain string

    Example:
        response = ask_llm("What is 2+2?")
        → "4"
    """
    client = get_groq_client()

    chat_completion = client.chat.completions.create(
        model=settings.groq_model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return chat_completion.choices[0].message.content.strip()


def ask_llm_with_history(
    messages: list[dict],
    system_prompt: str = "You are a helpful assistant.",
    temperature: float = 0.1,
    max_tokens: int = 1000,
) -> str:
    """
    Sends a full conversation history to the LLM.
    Useful for multi-turn conversations.

    Args:
        messages: List of {"role": "user"/"assistant", "content": "..."}
        system_prompt: Instructions for the model
        temperature: Creativity level
        max_tokens: Maximum response length

    Returns:
        The model's response as a plain string
    """
    client = get_groq_client()

    full_messages = [
        {"role": "system", "content": system_prompt},
        *messages,
    ]

    chat_completion = client.chat.completions.create(
        model=settings.groq_model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=full_messages,
    )

    return chat_completion.choices[0].message.content.strip()