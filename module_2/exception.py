import logging

logger = logging.getLogger(__name__)


def throw_err() -> NotImplementedError:
    raise


def send_message_with_retry(
    promt: str, max_retries: int = 3, base_delay: float = 1.0
) -> str | None:
    try:
        response = "Hi there"
    except NotImplementedError:
        send_message_with_retry(promt, max_retries, base_delay)
    else:
        print(response)
    finally:
        print("Hello")


send_message_with_retry("He", 3, 1)


def load_document(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def split_into_chunks(doc: str) -> list[str]:
    return []


def process_document(filepath: str) -> list[str]:
    try:
        doc = load_document(filepath)
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except UnicodeDecodeError:
        raise
    else:
        return split_into_chunks(doc)

