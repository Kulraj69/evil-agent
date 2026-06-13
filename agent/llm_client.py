"""
LLM clients for the self-correcting agent.

Two implementations share one interface:

    complete(messages: list[dict], run_id: str, **kwargs) -> dict
        returns {"content": str, "input_tokens": int, "output_tokens": int, "cost_usd": float}

  * AzureOpenAIClient - real reasoning via Azure OpenAI (reads .env).
  * make_llm_client() - factory that returns the Azure client if credentials
    are configured, otherwise None (callers fall back to their offline stand-in).

This keeps the agent code identical whether it runs live or offline.
"""

import os
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


SYSTEM_PROMPT = (
    "You are a senior digital-forensics and incident-response (DFIR) analyst. "
    "You reason carefully about evidence, never invent artifacts, and only make "
    "claims you can tie to specific evidence provided to you. When asked for JSON, "
    "respond with ONLY a JSON object or array in a ```json code block."
)


class AzureOpenAIClient:
    """Real LLM client backed by Azure OpenAI chat completions."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        deployment: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.api_version = api_version or os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

        self.input_cost = float(os.getenv("LLM_INPUT_COST_PER_1K", "0") or 0)
        self.output_cost = float(os.getenv("LLM_OUTPUT_COST_PER_1K", "0") or 0)

        if not (self.endpoint and self.api_key and self.deployment):
            raise ValueError(
                "Azure OpenAI not configured. Set AZURE_OPENAI_ENDPOINT, "
                "AZURE_OPENAI_API_KEY and AZURE_OPENAI_DEPLOYMENT in .env."
            )

        from openai import AzureOpenAI  # imported lazily so offline runs need no dep
        self._client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version,
        )

    def complete(self, messages: List[Dict[str, str]], run_id: str, **kwargs) -> Dict[str, Any]:
        full_messages = [{"role": "system", "content": SYSTEM_PROMPT}, *messages]
        resp = self._client.chat.completions.create(
            model=self.deployment,
            messages=full_messages,
            temperature=kwargs.get("temperature", 0.1),
            max_tokens=kwargs.get("max_tokens", 1200),
        )
        content = resp.choices[0].message.content or ""
        usage = getattr(resp, "usage", None)
        input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
        output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0
        cost = round(
            (input_tokens / 1000.0) * self.input_cost + (output_tokens / 1000.0) * self.output_cost,
            6,
        )
        return {
            "content": content,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost,
        }


def make_llm_client() -> Optional["AzureOpenAIClient"]:
    """
    Return a configured AzureOpenAIClient, or None if credentials are missing
    or the openai package isn't installed. Callers should fall back to their
    offline reasoning stand-in when this returns None.
    """
    if not (os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY")
            and os.getenv("AZURE_OPENAI_DEPLOYMENT")):
        return None
    try:
        return AzureOpenAIClient()
    except Exception as exc:  # missing dep, bad config, etc.
        print(f"[llm] Azure OpenAI unavailable ({exc}); using offline reasoning.")
        return None
