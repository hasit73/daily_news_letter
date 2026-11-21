from daily_news_letter.models import NewsArticle, NewsAggregationState
from daily_news_letter.api import NewsApiSearch, CurrentNewsApiSearch


def collect_news_from_news_api_org(state: NewsAggregationState) -> NewsAggregationState:
    """Collect news from https://newsapi.org/v2 source."""
    try:
        queries = state["search_queries"]
        news = NewsApiSearch().get_news(queries)
        news_articles = [
            NewsArticle(
                **(
                    {
                        "headline": article.get("title"),
                        "sub_headline": article.get("description"),
                        "content": article.get("content"),
                        "author": article.get("author"),
                        "metadata": {"source": article.get("source", {}).get("name")},
                        "published_at": article.get("publishedAt"),
                        "url": article.get("url"),
                    }
                )
            )
            for article in news.get("data")
        ]
        return {"news": news_articles}
    except Exception as err:
        print(err)
    return {"news": []}


def collect_news_from_current_news_api(
    state: NewsAggregationState,
) -> NewsAggregationState:
    """Collect news from https://api.currentsapi.services/v1 source."""
    try:
        ai_news = CurrentNewsApiSearch().get_ai_news().get("data", [])
        # latest_news = CurrentNewsApiSearch().get_latest_news().get("data", [])
        latest_news = []
        news = []
        included_news_id = set()
        for article in ai_news + latest_news:
            if article.get("id") in included_news_id:
                continue

            news.append(
                NewsArticle(
                    **(
                        {
                            "headline": article.get("title"),
                            "content": article.get("description"),
                            "author": article.get("author"),
                            "metadata": {"categories": article.get("category", [])},
                            "published_at": article.get("published"),
                            "url": article.get("url"),
                        }
                    )
                )
            )
        return {"news": news}
    except Exception as err:
        print(err)
    return {"news": []}


def collect_news(state: NewsAggregationState):
    """Placeholder node added for better representation."""
    pass
