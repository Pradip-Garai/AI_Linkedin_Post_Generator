from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

_llm = None


def get_llm():
    global _llm
    if _llm is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        _llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.1-8b-instant",
            temperature=0.7
        )
    return _llm


# ✅ Export real Runnable (NOT property)
llm = get_llm()


if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients of Panipuri?")
    print(response.content)
