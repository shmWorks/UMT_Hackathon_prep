"""
LLM Client Module
Provides unified interface for OpenAI and Google Gemini models.
"""
import sys
sys.path.append(str(__file__).rsplit("src", 1)[0])
from config import LLM_PROVIDER, LLM_MODEL, OPENAI_API_KEY, GOOGLE_API_KEY


def get_llm():
    """
    Returns a LangChain LLM instance based on configuration.
    
    Returns:
        A ChatOpenAI or ChatGoogleGenerativeAI instance.
    """
    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=LLM_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.1  # Low for consistent outputs
        )
    elif LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.1
        )
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")


def invoke_llm(prompt: str) -> str:
    """
    Simple helper to invoke the LLM with a string prompt.
    
    Args:
        prompt: The prompt string.
        
    Returns:
        The LLM's response as a string.
    """
    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content
