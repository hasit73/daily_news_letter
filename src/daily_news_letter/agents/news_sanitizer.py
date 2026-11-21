from daily_news_letter.models import NewsAggregationState
from daily_news_letter.common import sanitize_html, normalize_datetime


def sanitize_news(state: NewsAggregationState):
    """Sanitize news article content (headline, sub headline, and content) to remove any HTML tags and standardize datetime format."""
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
