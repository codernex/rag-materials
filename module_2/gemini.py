from abs_llm_client import AbstractLLMCLient
from google import genai


class Gemini(AbstractLLMCLient):
    _client: genai.Client

    def __int__(self):
        self._client = genai.Client(api_key="")

    def send_message(self, promt: str) -> str:
        try:
            response = self._client.models.generate_content(
                model="gemini-3-flash", contents=promt
            )
        except ResourceWarning:
            raise

        else:
            return response.text
