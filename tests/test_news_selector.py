from conftest import make_article

from daily_news_letter.agents.news_selector import MAX_SELECTED_NEWS, news_selector


def _select(articles):
    return news_selector({"sanitized_news": articles})["sanitized_news"]


def test_sorts_most_recent_first_and_puts_undated_last():
    articles = [
        make_article(url="u1", headline="old", published_at="2025-01-01T00:00:00+00:00"),
        make_article(url="u2", headline="undated", published_at=""),
        make_article(url="u3", headline="new", published_at="2025-03-01T00:00:00+00:00"),
    ]
    assert [a.headline for a in _select(articles)] == ["new", "old", "undated"]


def test_drops_articles_without_content():
    assert _select([make_article(content="")]) == []


def test_dedupes_by_url_and_by_headline():
    articles = [
        make_article(url="https://a", headline="Story A"),
        make_article(url="https://a", headline="Story A (syndicated)"),
        make_article(url="https://b", headline="  story a "),
        make_article(url="https://c", headline="Story C"),
    ]
    assert [a.url for a in _select(articles)] == ["https://a", "https://c"]


def test_caps_number_of_selected_articles():
    articles = [
        make_article(url=f"https://e.com/{i}", headline=f"Story {i}")
        for i in range(MAX_SELECTED_NEWS + 10)
    ]
    assert len(_select(articles)) == MAX_SELECTED_NEWS
