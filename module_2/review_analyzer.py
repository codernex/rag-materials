from prompt_engine import PromptEngine, LLMClient
from typing import Any


class ReviewAnalyzer:
    """
    Analyzes product reviews using structured prompt engineering.

    For each review, extracts:
    - sentiment: positive | neutral | negative
    - rating_prediction: 1-5 (integer)
    - key_topics: list of up to 3 main topics mentioned
    - would_recommend: yes | no | unclear

    Additionally maintains a session summary that tracks:
    - total reviews analyzed
    - sentiment distribution (how many positive/neutral/negative)
    - average predicted rating
    """

    def __init__(
        self,
    ) -> None:
        self._engine = PromptEngine(
            LLMClient(system_prompt="You are a senior product data engineer")
        )
        self.sessions: list[dict[str, Any]] = []
        pass

    def analyze(self, review_text: str) -> dict[str, str | int | list[str]]:
        """
        Analyze a single review and return structured insights.
        Must use PromptEngine.extract internally.
        """
        data = self._engine.extract(
            review_text,
            {
                "sentiment": "positive|neutral|negative",
                "rating_prediction": "integer between 1 and 5",
                "key_topics": "list of up to 3 main topics",
                "would_recommend": "yes|no|unclear",
            },
        )
        self.sessions.append(data)
        return data

    def get_session_summary(self) -> dict[str, Any]:
        """
        Return aggregated statistics across all analyzed reviews.
        Must derive average_rating from raw data, not a running total.
        """
        total_reviews = len(self.sessions)
        if total_reviews == 0:
            return {"average_rating": 0}
        total_rating = 0
        positive = 0
        negative = 0
        for data in self.sessions:
            total_rating += data.get("rating_prediction")
            if data.get("sentiment") == "positive":
                positive += 1
            elif data.get("sentiment") == "negative":
                negative += 1
        pass

        return {
            "average_rating": total_rating / total_reviews,
            "total_reviews": total_reviews,
            "sentiment_distribution": {"positive": positive, "negative": negative},
        }
