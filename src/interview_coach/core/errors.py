class LLMError(Exception):
    """Raised when the LLM provider fails, times out, or returns something unusable."""