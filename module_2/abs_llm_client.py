from abc import ABC, abstractmethod


class AbstractLLMCLient(ABC):

    @abstractmethod
    def send_message(self, promt: str) -> str:
        """
        Sends a prompt to the LLM and returns the response.
        Args:
            prompt: the actual prompt
        Returns:
            return the response from the llm
        """
        pass
