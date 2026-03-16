from llm_client import LLMClient


class ModelComparator:
    """
    Sends identical messages to two LLM clients and compares responses.

    Maintains two internal clients:
    - client_a: configured with system_prompt_a
    - client_b: configured with system_prompt_b

    For each comparison:
    - Send the same message to both clients
    - Store both responses as a pair
    - Track response lengths for averaging
    """

    def __init__(self, system_prompt_a: str, system_prompt_b: str) -> None:
        self._client_a = LLMClient(system_prompt_a)
        self._client_b = LLMClient(system_prompt_b)
        self._response_pairs: list[dict[str, str]] = []

    def compare(self, message: str) -> dict[str, str]:
        """
        Send message to both clients and return both responses.

        Returns:
            dict with keys 'a' and 'b' mapping to each response
        """
        response_a = self._client_a.send_message(message)
        response_b = self._client_b.send_message(message)

        data = {"a": response_a, "b": response_b}
        self._response_pairs.append(data)
        return data

    def get_comparisons(self) -> list[dict[str, str]]:
        """Return all comparison pairs collected so far."""
        return self._response_pairs.copy()

    def average_response_length(self) -> dict[str, float]:
        """
        Return average response length in characters for each client.

        Returns:
            dict with keys 'a' and 'b' mapping to average lengths.
            Returns 0.0 if no comparisons have been made yet.
        """
        if len(self._response_pairs) == 0:
            return {"a": 0.0, "b": 0.0}
        total_a = 0
        total_b = 0
        for pair in self._response_pairs:
            a_response = pair.get("a", "")
            b_response = pair.get("b", "")

            total_a += len(a_response)
            total_b += len(b_response)
        count = len(self._response_pairs)
        return {"a": total_a / count, "b": total_b / count}
