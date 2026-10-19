import httpx
import pytest

from interview_coach.core.errors import LLMError
from interview_coach.llm.client import OpenRouterClient


def make_client(handler: httpx.MockTransport) -> OpenRouterClient:
    return OpenRouterClient(
        api_key="test-key",
        base_url="https://test.local/api/v1",
        default_model="test/model",
        transport=handler,
    )


async def test_complete_returns_message_content() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json={"choices": [{"message": {"content": "Hello!"}}]}
        )

    client = make_client(httpx.MockTransport(handler))
    result = await client.complete([{"role": "user", "content": "Hi"}])
    assert result == "Hello!"
    await client.aclose()