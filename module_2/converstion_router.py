from llm_client import LLMClient


class ConversationRouter:
    def __init__(self) -> None:
        self._technical = LLMClient("You are a senior software engineer")
        self._creative = LLMClient("You are a creative expert")
        self._general = LLMClient("You are a helpful assistant")
        self._technical_keyword = ["code", "function", "bug"]
        self._creative_keyword = ["write", "story", "poem"]
        self._llm_used: list[str] = []

    def route(self, message: str) -> str:
        if any(word in message for word in self._technical_keyword):
            self._llm_used.append("technical")
            return self._technical.send_message(message)
        elif any(word in message for word in self._creative_keyword):
            self._llm_used.append("creative")
            return self._creative.send_message(message)
        else:
            self._llm_used.append("general")
            return self._general.send_message(message)

    def get_routing_log(self) -> list[str]:
        return self._llm_used.copy()

    def get_routing_stats(self) -> dict[str, int]:
        return {
            "technical": self._llm_used.count("technical"),
            "creative": self._llm_used.count("creative"),
            "general": self._llm_used.count("general"),
        }
