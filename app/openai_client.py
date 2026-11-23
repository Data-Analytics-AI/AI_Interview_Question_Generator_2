'''# app/openai_client.py
import os
import openai
from .config import settings
from typing import Any, Dict

# Configure OpenAI SDK for Azure
openai.api_type = "azure"
openai.api_base = settings.azure_openai_endpoint.rstrip("/")
openai.api_key = settings.azure_openai_key
openai.api_version = settings.azure_openai_api_version

DEPLOYMENT_NAME = settings.azure_openai_deployment

def generate_completion(prompt: str, temperature: float = 0.2, max_tokens: int = 800) -> str:
    """
    Use Azure OpenAI deployment to generate text.
    """
    resp = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates structured interview questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # ChatCompletion returns choices -> message
    return resp["choices"][0]["message"]["content"]

# app/openai_client.py
import os
import asyncio
from typing import Any
from openai import OpenAI
from .config import settings

# Create a single shared client
# The OpenAI client will read API key from env or accept it directly.
# For Azure, we pass 'base_url' and set api_type to 'azure' if the library supports it.
client = OpenAI(
    api_key=settings.azure_openai_key,
    base_url=settings.azure_openai_endpoint.rstrip("/"),
)
# Initialize Azure OpenAI client


async def generate_completion(
    prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 900,
    deployment: str | None = None,
) -> str:
    """
    Use Azure OpenAI chat completion via the OpenAI client asynchronously.
    `deployment` should be the Azure deployment name for the model.
    """
    # `client.chat.completions.create` is async-friendly in modern SDKs.
    # We pass 'model' as deployment name for Azure-style deployments.
    deployment = deployment or settings.azure_openai_deployment
    resp = await client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are an expert interviewer that returns structured interview questions in JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    # The response shape may vary; adapt as necessary.
    # Try to extract the assistant text
    try:
        return resp.choices[0].message.content
    except Exception:
        # Fallback: string representation
        return str(resp)'''

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
#from azure.openai import AzureOpenAI
from .config import settings

load_dotenv()

# Initialize Azure OpenAI client using the user's format
'''client = AzureOpenAI(
    api_key=settings.azure_openai_key,
    api_version=settings.azure_openai_api_version,
    azure_endpoint=settings.azure_openai_endpoint
)

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

async def generate_completion(prompt: str):
    """
    Sends a chat completion request to Azure OpenAI and returns the generated text.
    """

    response = client.chat.completions.create(
        model=settings.azure_openai_deployment,
        messages=[
            {"role": "system", "content": "You are an AI assistant that generates structured interview questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800,
    )

    # Extract response text
    return response.choices[0].message.content#response.choices[0].message["content"]'''

# app/openai_client.py

from openai import AzureOpenAI
from .config import settings

client = AzureOpenAI(
    api_key=settings.azure_openai_key,
    api_version=settings.azure_openai_api_version,
    azure_endpoint=settings.azure_openai_endpoint
)

DEPLOYMENT = settings.azure_openai_deployment


def generate_completion(prompt: str, temperature: float = 0.2, max_tokens: int = 3500) -> str:
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content



