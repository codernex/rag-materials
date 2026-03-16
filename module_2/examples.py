from openai import OpenAI, RateLimitError, APITimeoutError
import json


def extract_product_info(review: str) -> dict[str, str]:
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Extract product name and price as JSON.",
                },
                {"role": "user", "content": review},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
    except (RateLimitError, APITimeoutError) as e:
        raise RuntimeError(f"failed to compete the chat") from e
    else:
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse the json") from e

    if "price" not in result:
        raise ValueError("Missing required field price")
    if "name" not in result:
        raise ValueError("Missing required field name")
    return result
