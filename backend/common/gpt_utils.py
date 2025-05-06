import os
import requests
from dotenv import load_dotenv
from common.logging_utils import logger

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"  # or any other available model


def get_chatgpt_response(system_prompt: str, user_prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            logger.exception(response.text)
            raise ValueError("Invalid request to Groq API. Please check the prompt or formatting.")

        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.HTTPError as e:
        error_content = response.text if response else str(e)
        raise RuntimeError(f"GROQ API Error {response.status_code if response else 'Unknown'}: {error_content}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error calling GROQ API: {e}")
