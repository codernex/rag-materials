import logging

type Messages = list[dict[str, str]]

logger = logging.getLogger(__name__)


class LLMClient:
    model: str = "gpt-4o"
    api_key: str = ""
    message_histories: Messages = []
    request_count: int = 0

    def __init__(
        self,
        apiKey: str,
        model: str = "gpt-4o",
        sytem_prompt: str | None = None,
        max_retries: int = 3,
    ) -> None:
        self.api_key = apiKey
        self.sytem_prompt = sytem_prompt or "You are a helpful assistant"
        self.max_retries = max_retries
        self.request_count = 0

        if model:
            model = model

    def sendMessage(self, promt: str) -> str | None:
        LLMClient.request_count += 1

    def getHistory(self) -> Messages:
        return self.message_histories.copy()

    def logRequests(self) -> str | None:
        pass

    def handleError(self) -> None:
        pass


client1 = LLMClient("12424", "gpt-3.5-turbo")
client2 = LLMClient("12424", "gpt-3.5-turbo")

client1.sendMessage("Hi who is there?")
client2.sendMessage("Hi who is there?")

print(LLMClient.request_count)
