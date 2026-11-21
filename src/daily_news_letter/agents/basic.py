from daily_news_letter.models import NewsAggregationState


def news_aggregator(state: NewsAggregationState) -> NewsAggregationState:
    """Join point for the parallel collectors.

    `news` uses an `operator.add` reducer, so the collectors' results are already
    merged here. Returning `news` again would append the list to itself.
    """
    print("📋 Collected total news records : ", len(state["news"]))
    return {}
