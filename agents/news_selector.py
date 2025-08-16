from daily_news_letter.models import NewsExtractorState


def news_selector(state: NewsExtractorState):
    """Stratigically select news which are relevant for end users. To keep it simple for now - we are selecting top 30 headlines."""
    news = state["sanitized_news"][:30]
    print("Total selected news : ", len(news))
    return {"sanitized_news": news}
