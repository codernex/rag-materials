import json
import logging
from typing import Any
from llm_client import LLMClient, APITimeoutError, RateLimitError

logger = logging.getLogger(__name__)


class PromptEngine:
    """
    A reusable prompt engineering library built on top of LLMClient.

    Encapsulates zero-shot, few-shot, and structured output extraction
    patterns. Composes with LLMClient rather than inheriting from it.
    """

    def __init__(self, client: LLMClient) -> None:
        """
        Initialize PromptEngine with a shared client and a dedicated
        extraction client with temperature=0.

        Args:
            client: LLMClient instance for zero-shot and few-shot tasks.
        """
        self._client = client
        # Dedicated client for extraction — temperature=0 is non-negotiable
        # for structured output tasks and must not be overridable by callers
        self._extraction_client = LLMClient(
            system_prompt="You are a precise data extraction assistant.", temperature=0
        )

    def zero_shot(self, task_description: str, input_text: str) -> str:
        """
        Send a zero-shot prompt to the LLM.

        Args:
            task_description: Instruction describing what the model should do.
            input_text: The text to process.

        Returns:
            Model response as a string.
        """
        # Simple concatenation — no examples, just task + input
        return self._client.send_message(f"{task_description}\n\n{input_text}")

    def few_shot(
        self, task_description: str, examples: list[tuple[str, str]], input_text: str
    ) -> str:
        """
        Send a few-shot prompt with examples to guide output format.

        Args:
            task_description: Instruction describing the task.
            examples: List of (input, output) demonstration pairs.
            input_text: The actual input to process.

        Returns:
            Model response as a string.
        """
        prompt_parts = [task_description.strip(), ""]

        for i, (ex_input, ex_output) in enumerate(examples, start=1):
            prompt_parts.append(f"Example {i}:")
            prompt_parts.append(f"Input: {ex_input}")
            prompt_parts.append(f"Output: {ex_output}")
            prompt_parts.append("")

        prompt_parts.append("Now complete the following:")
        prompt_parts.append(f"Input: {input_text}")
        prompt_parts.append("Output:")

        return self._client.send_message("\n".join(prompt_parts))

    def extract(self, input_text: str, schema: dict[str, Any]) -> dict[str, Any]:
        """
        Extract structured data from text using the provided schema.

        Retries up to 3 total attempts on JSON or schema failures,
        feeding error context back into each retry prompt.

        Args:
            input_text: The unstructured text to extract from.
            schema: Dict mapping field names to their expected format.

        Returns:
            Validated dict containing all schema keys.

        Raises:
            RuntimeError: If all retry attempts are exhausted.
        """
        last_error: str | None = None

        for attempt in range(3):
            prompt = self._build_schema_prompt(input_text, schema, last_error)

            try:
                response = self._extraction_client.send_message(prompt)
            except (APITimeoutError, RateLimitError) as e:
                # Transient failures — log and retry
                last_error = f"API call failed: {e}"
                logger.warning("Attempt %d API failure: %s", attempt + 1, e)
                continue

            try:
                result = json.loads(response)
            except json.JSONDecodeError as e:
                last_error = f"Your response was not valid JSON: {e}"
                logger.warning("Attempt %d JSON parse failed", attempt + 1)
                continue

            try:
                self._validate_schema(result, schema)
            except ValueError as e:
                last_error = f"Your response was missing required fields: {e}"
                logger.warning("Attempt %d schema validation failed", attempt + 1)
                continue

            # Only reached if all checks passed
            return result

        raise RuntimeError(
            f"Extraction failed after 3 attempts. Last error: {last_error}"
        )

    def _build_schema_prompt(
        self, input_text: str, schema: dict[str, str], last_error: str | None
    ) -> str:
        """
        Build the structured extraction prompt.

        Includes error context on retry attempts so the model
        knows what went wrong and can correct its response.

        Args:
            input_text: The text to extract from.
            schema: Expected output schema.
            last_error: Error message from previous attempt, if any.

        Returns:
            Complete prompt string ready for the API.
        """
        prompt_parts = [
            "Extract the requested information from the input text.",
            f"Respond with valid JSON only matching this schema: {schema}",
            "No text before or after the JSON.",
            f"\nInput: {input_text}",
        ]

        if last_error is not None:
            prompt_parts.append(
                f"\nYour previous attempt failed with this error: {last_error}"
                f"\nPlease correct your response."
            )

        return "\n".join(prompt_parts)

    def _validate_schema(self, data: dict, schema: dict[str, str]) -> None:
        """
        Validate that all schema keys are present in the parsed response.

        Args:
            data: Parsed dict from model response.
            schema: Expected schema with required field names as keys.

        Raises:
            ValueError: If any required field is missing from data.
        """
        missing = [key for key in schema if key not in data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")


# ```

# ---

# ### 📖 Reading Alignment

# Your `_build_schema_prompt` method embodies what the DAIR.AI prompt engineering guide described as the core principle of few-shot prompting — showing the model exactly what format you expect. Your error-injection on retry is a production pattern that the guide doesn't cover but emerges naturally from first principles: if the model failed, tell it specifically how it failed. That's good engineering reasoning applied to prompt design.

# ---

# ## Lab Result: Passed ✅
# ```
# Correctness:          47/50
# Code Quality:          7/10
# Production Readiness:  8/10
# Reading Alignment:     5/5

# Total: 67/75
