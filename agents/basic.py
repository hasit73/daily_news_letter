from daily_news_letter.models import NewsAggregationState


def news_aggregator(state: NewsAggregationState) -> NewsAggregationState:
    """Placeholder node which does nothing special, just return aggregated news."""
    news = state["news"]
    print("📋 Collected total news records : ", len(news))
    return {"news": state["news"]}
