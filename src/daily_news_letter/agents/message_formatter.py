from jinja2 import Template

from daily_news_letter.common import MAX_MESSAGE_CHAR_LIMIT, MESSAGE_SEPARATOR
from daily_news_letter.models import NewsExtractorState
from daily_news_letter.prompts import WHATSAPP_MESSAGE_FORMAT

# WhatsApp messages are plain text: HTML-escaping would turn "&" into "&amp;".
_TEMPLATE = Template(WHATSAPP_MESSAGE_FORMAT, autoescape=False)
_ELLIPSIS = "…"


def _render(article, content: str) -> str:
    return _TEMPLATE.render(
        headline=article.headline,
        sub_headline=article.sub_headline,
        content=content,
        published_at=article.published_at,
        url=article.url,
    ).strip()


def _render_within_limit(article, limit: int) -> str:
    """Render an article, truncating its content if the result exceeds `limit`."""
    formatted = _render(article, article.content)
    overflow = len(formatted) - limit
    if overflow <= 0:
        return formatted
    keep = max(len(article.content) - overflow - len(_ELLIPSIS), 0)
    return _render(article, article.content[:keep].rstrip() + _ELLIPSIS)[:limit]


def format_whatsapp_messages(state: NewsExtractorState):
    """Group enriched articles into WhatsApp messages.

    Each output message is a list of formatted articles whose joined length
    (including separators) stays within the WhatsApp message size limit.
    """
    output_messages: list[list[str]] = []
    current: list[str] = []
    current_size = 0

    for article in state["enriched_news"]:
        formatted = _render_within_limit(article, MAX_MESSAGE_CHAR_LIMIT)
        added_size = len(formatted) + (len(MESSAGE_SEPARATOR) if current else 0)
        if current and current_size + added_size > MAX_MESSAGE_CHAR_LIMIT:
            output_messages.append(current)
            current, current_size = [], 0
            added_size = len(formatted)
        current.append(formatted)
        current_size += added_size

    if current:
        output_messages.append(current)
    return {"output_messages": output_messages}
