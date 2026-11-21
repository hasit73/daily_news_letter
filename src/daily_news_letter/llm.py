from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI

GEMINI_MODEL = "gemini-2.0-flash-lite"


@lru_cache(maxsize=1)
def get_llm() -> ChatGoogleGenerativeAI:
    """Create the Gemini client lazily so importing the package doesn't require
    GOOGLE_API_KEY (e.g. in mock mode or tests)."""
    return ChatGoogleGenerativeAI(model=GEMINI_MODEL)
