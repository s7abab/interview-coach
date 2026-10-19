from typing import Protocol, TypedDict

import httpx
from interview_coach.core.errors import LLMError


class Message(TypedDict):
    role: str  # "system" | "user" | "assistant"
    content: str


class LLMClient(Protocol):
    async def complete(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        temperature: float = 0.2,
    ) -> str: ...


class OpenRouterClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        default_model: str,
        timeout: float = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._default_model = default_model
        self._http = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
            transport=transport,
        )

    async def complete(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        payload = {
            "model": model or self._default_model,
            "messages": messages,
            "temperature": temperature,
        }
        try:
            response = await self._http.post("/chat/completions", json=payload)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise LLMError("LLM request timed out") from exc
        except httpx.HTTPStatusError as exc:
            raise LLMError(f"LLM returned status {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            raise LLMError("Network error calling LLM") from exc

        try:
            return str(response.json()["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMError("Unexpected response shape from LLM") from exc

    async def aclose(self) -> None:
        await self._http.aclose()