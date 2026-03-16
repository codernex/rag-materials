from llm_client import LLMClient


class SummarizerClient(LLMClient):
    def __init__(self, max_retries: int = 3) -> None:
        super().__init__("You are helpful summarizer", max_retries)
        self.summaries: list[str] = []

    def summarize(self, document: str) -> str:
        """
        Summarize a doucment and store the result

        Args:
            document: The text to summarize
        Returns:
            A concise summary as a string
        """
        result = self.send_message(
            f"Please summarize the following document concisely:\n\n{document}"
        )
        self.summaries.append(result)
        return result

    def get_all_summaries(self) -> list[str]:
        """Return all summaries produced in this session."""
        return self.summaries.copy()

    def total_documents_summarized(self) -> int:
        """Return how many documents have been summarized."""
        return len(self.summaries)
