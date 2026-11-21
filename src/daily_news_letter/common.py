import os
from dateutil import parser
from datetime import timezone
from html_sanitizer import Sanitizer


# Constants
MAX_MESSAGE_CHAR_LIMIT = 4080
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA") != "false"


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


sanitizer = Sanitizer()


def normalize_datetime(date_str: str):
    try:
        dt = parser.parse(date_str)  # auto-detects format and timezone
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.isoformat()
    except (ValueError, TypeError, OverflowError, Exception) as e:
        print(f"Failed to parse datetime '{date_str}': {e}")
        return ""


def sanitize_html(html_str):
    if not html_str:
        return ""
    cleaned_html = sanitizer.sanitize(html_str)
    return cleaned_html
