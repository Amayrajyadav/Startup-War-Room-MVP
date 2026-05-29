import os
from openai import AsyncOpenAI

# Initialize the OpenAI client for LM Studio
# LM Studio runs a local server that mimics the OpenAI API format
client = AsyncOpenAI(
    base_url=os.getenv("LM_STUDIO_API_BASE", "http://localhost:1234/v1"),
    api_key=os.getenv("LM_STUDIO_API_KEY", "not-needed")
)

async def generate_response(system_prompt: str, user_prompt: str) -> str:
    """
    Calls the local Gemma model via LM Studio's OpenAI-compatible API.
    Provides a reusable interface for all stakeholder agents.
    """
    try:
        response = await client.chat.completions.create(
            model="local-model",  # LM Studio ignores this field, but it's required by the client
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        
        return response.choices[0].message.content or ""
        
    except Exception as e:
        print(f"Error calling local LLM: {e}")
        return f"Error: Unable to reach the local LLM. Check if LM Studio is running. ({str(e)})"
