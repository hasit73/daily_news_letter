from daily_news_letter.models import NewsExtractorState

MAX_SELECTED_NEWS = 30


def news_selector(state: NewsExtractorState):
    """Select the articles to include in the newsletter.

    Drops articles without content, removes duplicates reported by more than one
    source (same URL or headline), and keeps the most recent MAX_SELECTED_NEWS.
    """
    seen = set()
    candidates = []
    for article in state["sanitized_news"]:
        if not article.content:
            continue
        keys = {article.url, article.headline.strip().lower()} - {None, ""}
        if keys & seen:
            continue
        seen |= keys
        candidates.append(article)

    # ISO-8601 UTC strings sort chronologically; unparseable dates ("") go last.
    candidates.sort(key=lambda a: a.published_at, reverse=True)
    news = candidates[:MAX_SELECTED_NEWS]
    print("Total selected news : ", len(news))
    return {"sanitized_news": news}
