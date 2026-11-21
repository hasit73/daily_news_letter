import os
import re
from datetime import timezone
from html.parser import HTMLParser

from dateutil import parser

# Constants
MAX_MESSAGE_CHAR_LIMIT = 4080
MESSAGE_SEPARATOR = "\n\n"
REQUEST_TIMEOUT_SECONDS = 15


def use_mock_data() -> bool:
    """Read USE_MOCK_DATA at call time so .env loading order and tests don't matter."""
    return os.getenv("USE_MOCK_DATA", "false").strip().strip("\"'").lower() in {
        "1",
        "true",
        "yes",
    }


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


# Graph nodes list
class Nodes:
    SEARCH_QUERY_BUILDER = "search_query_builder"
    COLLECT_NEWS = "collect_news"
    COLLECT_NEWS_FROM_NEWS_API_ORG = "collect_news_from_news_api_org"
    COLLECT_NEWS_FROM_CURRENT_NEWS_API = "collect_news_from_current_news_api"
    NEWS_AGGREGATOR = "news_aggregator"
    SANITIZE_NEWS = "sanitize_news"
    NEWS_SELECTOR = "news_selector"
    NEWS_ENRICHER = "news_enricher"
    FORMAT_WHATSAPP_MESSAGES = "format_whatsapp_messages"


def normalize_datetime(date_str: str) -> str:
    """Parse any reasonable datetime string and return it as an ISO-8601 UTC string.

    Naive datetimes are assumed to already be in UTC. Returns "" if unparseable.
    """
    try:
        dt = parser.parse(date_str)
    except (ValueError, TypeError, OverflowError) as e:
        print(f"Failed to parse datetime '{date_str}': {e}")
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


class _TextExtractor(HTMLParser):
    _SKIP_TAGS = {"script", "style"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self._SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            self.parts.append(data)


_TRUNCATION_MARKER = re.compile(r"\s*\[\+\d+ chars\]\s*$")


def sanitize_html(html_str: str | None) -> str:
    """Convert an HTML fragment to plain text suitable for a WhatsApp message.

    Strips all tags (dropping script/style content), decodes entities, removes
    NewsAPI's "[+1234 chars]" truncation marker and collapses whitespace.
    """
    if not html_str:
        return ""
    extractor = _TextExtractor()
    extractor.feed(html_str)
    extractor.close()
    text = "".join(extractor.parts)
    text = _TRUNCATION_MARKER.sub("", text)
    return re.sub(r"\s+", " ", text).strip()
