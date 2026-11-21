from pydantic import ValidationError

from daily_news_letter.api import CurrentNewsApiSearch, NewsApiSearch
from daily_news_letter.models import NewsAggregationState, NewsArticle


def _build_articles(raw_articles: list[dict], to_fields) -> list[NewsArticle]:
    """Convert raw API articles, skipping individual invalid records instead of
    discarding the whole batch."""
    articles = []
    for raw in raw_articles:
        try:
            articles.append(NewsArticle(**to_fields(raw)))
        except ValidationError as err:
            print(f"Skipping invalid article {raw.get('url')}: {err.error_count()} error(s)")
    return articles


def _from_news_api_org(article: dict) -> dict:
    return {
        "headline": article.get("title"),
        "sub_headline": article.get("description"),
        # NewsAPI often returns content=null; fall back to the description.
        "content": article.get("content") or article.get("description") or "",
        "author": article.get("author"),
        "metadata": {"source": (article.get("source") or {}).get("name")},
        "published_at": article.get("publishedAt"),
        "url": article.get("url"),
    }


def _from_currents_api(article: dict) -> dict:
    return {
        "headline": article.get("title"),
        "content": article.get("description") or "",
        "author": article.get("author"),
        "metadata": {"categories": article.get("category", [])},
        "published_at": article.get("published"),
        "url": article.get("url"),
    }


def collect_news_from_news_api_org(state: NewsAggregationState) -> NewsAggregationState:
    """Collect news from https://newsapi.org/v2 source."""
    try:
        news = NewsApiSearch().get_news(state["search_queries"])
    except Exception as err:
        print(f"NewsAPI.org collection failed: {err}")
        return {"news": []}
    return {"news": _build_articles(news.get("data") or [], _from_news_api_org)}


def collect_news_from_current_news_api(
    state: NewsAggregationState,
) -> NewsAggregationState:
    """Collect news from https://api.currentsapi.services/v1 source."""
    try:
        raw_articles = CurrentNewsApiSearch().get_ai_news().get("data", [])
    except Exception as err:
        print(f"CurrentsAPI collection failed: {err}")
        return {"news": []}

    unique_articles = []
    seen_ids = set()
    for article in raw_articles:
        article_id = article.get("id") or article.get("url")
        if article_id in seen_ids:
            continue
        seen_ids.add(article_id)
        unique_articles.append(article)
    return {"news": _build_articles(unique_articles, _from_currents_api)}


def collect_news(state: NewsAggregationState):
    """Placeholder node that fans out to the individual news sources."""
    return {}
