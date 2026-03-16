import time
import logging
from openai import OpenAI, RateLimitError, APITimeoutError, AuthenticationError
import tiktoken

logger = logging.getLogger(__name__)


class LLMClient:
    """
    A production-grade client for the OpenAI chat completions API.

    Manages conversation history, retries on transient failures,
    and tracks request counts at both instance and class level.

    Class Attributes:
        default_system_prompt: Fallback prompt if none provided.
        total_request_count: Total successful requests across all instances.
    """

    default_system_prompt: str = "You are a helpful assistant"
    total_request_count: int = 0

    def __init__(
        self,
        system_prompt: str | None = None,
        max_retries: int = 3,
        temperature: float = 0,
    ) -> None:
        """
        Initialize the LLM client.

        Args:
            system_prompt: Instructions that define the model's behavior.
                           Falls back to default_system_prompt if not provided.
            max_retries: Maximum retry attempts on transient failures.
        """
        self.system_prompt: str = system_prompt or self.default_system_prompt
        self.message_history: list[dict[str, str]] = []
        self._client: OpenAI = OpenAI()
        self.max_retries: int = max_retries
        self.instance_request_count: int = 0
        self.temperature = temperature

    def _build_messages(self, prompt: str) -> list[dict[str, str]]:
        """
        Assemble the full message payload for the API call.

        Combines system prompt, conversation history, and the new
        user message. Does not modify history — read only.

        Args:
            prompt: The new user message to append.

        Returns:
            Complete message list ready for the API.
        """
        return [
            {"role": "system", "content": self.system_prompt},
            *self.message_history,
            {"role": "user", "content": prompt},
        ]

    def send_message(self, prompt: str) -> str:
        """
        Send a message and return the model's response.

        Retries up to max_retries times on rate limit or timeout
        errors using exponential backoff. Updates conversation
        history only on success.

        Args:
            prompt: The user's message.

        Returns:
            The model's response as a string.

        Raises:
            AuthenticationError: If the API key is invalid.
            RuntimeError: If all retry attempts are exhausted.
        """
        messages = self._build_messages(prompt)
        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                response = self._client.chat.completions.create(
                    model="gpt-4o", messages=messages, temperature=self.temperature
                )
                answer = response.choices[0].message.content

                # Guard against None response from model
                if answer is None:
                    raise RuntimeError("Model returned empty response")

            except AuthenticationError:
                # Bad API key will not fix itself — stop immediately
                logger.critical("Invalid API key — stopping immediately")
                raise

            except (RateLimitError, APITimeoutError) as e:
                last_error = e
                delay = 1.0 * (2**attempt)
                logger.warning(
                    "Attempt %d failed, retrying in %.1fs", attempt + 1, delay
                )
                time.sleep(delay)

            else:
                # Success — update history and counts only here
                self.message_history.append({"role": "user", "content": prompt})
                self.message_history.append({"role": "assistant", "content": answer})
                self.instance_request_count += 1
                LLMClient.total_request_count += 1
                return answer

        raise RuntimeError(
            f"Failed to get response after {self.max_retries} attempts"
        ) from last_error

    def get_history(self) -> list[dict[str, str]]:
        """
        Return a copy of the conversation history.

        Returns a copy to prevent external mutation of internal state.

        Returns:
            List of message dicts with role and content keys.
        """
        return self.message_history.copy()

    def clear_history(self) -> None:
        """
        Reset conversation history.

        Does not affect system prompt, client config, or request counts.
        """
        self.message_history = []

    def _count_token(self, text: str, model: str = "gpt-4o") -> int:
        encoder = tiktoken.encoding_for_model(model)
        return len(encoder.encode(text))
