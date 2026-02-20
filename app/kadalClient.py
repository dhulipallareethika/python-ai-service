import os
import httpx
import logging
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from app.handlers import LLMServiceError
from app.logger import log

load_dotenv()
AZURE_ENDPOINT = 'https://api.kadal.ai/proxy/api/v1/azure'
LM_KEY = os.getenv("LLM_API_KEY")
API_VERSION = "2024-02-15-preview"

if not LM_KEY:
    raise RuntimeError("LLM_API_KEY is missing from environment variables (.env)")

client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_version=API_VERSION,
    api_key=LM_KEY,
    timeout=30.0,
    max_retries=3,
    http_client=httpx.AsyncClient(verify=False) 
)

async def get_chat_completion(messages, correlation_id: str, model="gpt-4o-mini", temperature=0.7):
    log.info(
        f"Requesting completion from model {model}", 
        extra={'correlation_id': correlation_id}
    )
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        content = response.choices[0].message.content
        if not content:
            log.error(
                "LLM returned empty content", 
                extra={'correlation_id': correlation_id}
            )
            raise LLMServiceError("LLM returned an empty response.")
        log.info(
            "LLM response successfully received", 
            extra={'correlation_id': correlation_id}
        )
        return content
    except Exception as e:
        log.error(
            f"Kadal API Error: {str(e)}", 
            extra={'correlation_id': correlation_id}
        )
        raise LLMServiceError(f"Kadal API Error: {str(e)}")