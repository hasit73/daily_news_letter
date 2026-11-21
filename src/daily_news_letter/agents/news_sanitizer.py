from daily_news_letter.common import normalize_datetime, sanitize_html
from daily_news_letter.models import NewsAggregationState


def sanitize_news(state: NewsAggregationState):
    """Convert headline, sub-headline and content to plain text and normalize dates to UTC."""
    if not state.get("news"):
        return {"sanitized_news": []}
    news = state["news"]
    sanitized_news = []

    for article in news:
        sanitized_article = article.model_copy(
            update={
                "headline": sanitize_html(article.headline),
                "sub_headline": sanitize_html(article.sub_headline),
                "content": sanitize_html(article.content),
                "published_at": normalize_datetime(article.published_at),
            }
        )
        sanitized_news.append(sanitized_article)

    return {"sanitized_news": sanitized_news}
