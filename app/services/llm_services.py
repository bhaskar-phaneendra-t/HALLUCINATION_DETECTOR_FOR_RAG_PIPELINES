from app.core.logger import logger
from app.core.exception import CustomException
from app.core.config import LLM_PROVIDER, OLLAMA_BASE_URL, LLM_MODEL
import requests
import sys


def generate_response(query: str, docs: list = None):
    try:
        logger.info(f"Sending query to LLM: {query}")

        context = "\n".join(docs) if docs else ""

        prompt = f"""
You are a strict assistant.

Rules:
1. Answer ONLY from the provided context
2. If answer is not in context, say: "I don't know"
3. Do NOT use outside knowledge

Context:
{context}

Question:
{query}
"""

        if LLM_PROVIDER == "ollama":
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": LLM_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )

            data = response.json()

            # Safe handling
            if isinstance(data, dict):
                if "response" in data:
                    return data["response"]

                if "error" in data:
                    return f"ERROR: {data['error']}"

            return "ERROR: Invalid response from LLM"

        else:
            return "ERROR: Invalid LLM provider"

    except Exception as e:
        logger.error(f"Error in LLM service: {str(e)}")
        return "ERROR: LLM failed"