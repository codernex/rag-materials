import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TicketAnalysis:
    """Structured result of support ticket analysis."""

    urgency: str  # "low" | "medium" | "high"
    category: str  # "billing" | "technical" | "account"
    order_number: str | None
    sentiment: str  # "positive" | "neutral" | "negative"
    summary: str


def build_extraction_prompt(ticket_text: str) -> str:
    """
    Build a few-shot structured extraction prompt.

    Args:
        ticket_text: Raw support ticket text to analyze.

    Returns:
        Complete prompt string ready for the API.
    """
    return f"""Extract structured information from support tickets.
Respond with valid JSON only. No other text before or after.

Schema:
{{
  "urgency": "low" | "medium" | "high",
  "category": "billing" | "technical" | "account", 
  "order_number": <integer or null>,
  "sentiment": "positive" | "neutral" | "negative",
  "summary": "<max 20 words>"
}}

EXAMPLE INPUT:
"URGENT: Production server down, losing revenue. Ticket #9921"

EXAMPLE OUTPUT:
{{"urgency": "high", "category": "technical", "order_number": 9921, 
  "sentiment": "negative", "summary": "Production server down causing revenue loss"}}

NOW EXTRACT FROM:
"{ticket_text}"

JSON:"""


def validate_ticket_analysis(data: dict[str, str]) -> TicketAnalysis:
    """
    Validate parsed JSON against expected schema.

    Args:
        data: Parsed dictionary from LLM response.

    Returns:
        Validated TicketAnalysis dataclass instance.

    Raises:
        ValueError: If any required field is missing or invalid.
    """
    valid_urgencies = {"low", "medium", "high"}
    valid_categories = {"billing", "technical", "account"}
    valid_sentiments = {"positive", "neutral", "negative"}

    # Check required fields exist
    required = ["urgency", "category", "sentiment", "summary"]
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validate enum values
    if data["urgency"] not in valid_urgencies:
        raise ValueError(f"Invalid urgency: {data['urgency']}")
    if data["category"] not in valid_categories:
        raise ValueError(f"Invalid category: {data['category']}")
    if data["sentiment"] not in valid_sentiments:
        raise ValueError(f"Invalid sentiment: {data['sentiment']}")

    return TicketAnalysis(
        urgency=data["urgency"],
        category=data["category"],
        order_number=data.get("order_number"),  # optional field
        sentiment=data["sentiment"],
        summary=data["summary"],
    )
