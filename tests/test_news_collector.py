import pytest

from daily_news_letter import api
from daily_news_letter.agents.news_collector import (
    collect_news_from_current_news_api,
    collect_news_from_news_api_org,
)


def _news_api_article(**overrides):
    article = {
        "title": "Title",
        "description": "Description",
        "content": "Content",
        "author": "Author",
        "source": {"name": "Source"},
        "publishedAt": "2025-01-01T00:00:00Z",
        "url": "https://example.com/1",
    }
    article.update(overrides)
    return article


@pytest.fixture
def news_api_returns(monkeypatch):
    def _set(articles):
        monkeypatch.setattr(api.NewsApiSearch, "get_news", lambda self, queries: {"data": articles})

    return _set


def test_news_api_null_content_falls_back_to_description(news_api_returns):
    news_api_returns([_news_api_article(content=None)])
    [article] = collect_news_from_news_api_org({"search_queries": ["q"]})["news"]
    assert article.content == "Description"


def test_news_api_invalid_article_does_not_drop_the_batch(news_api_returns):
    news_api_returns(
        [
            _news_api_article(url="https://example.com/ok"),
            _news_api_article(title=None, url="https://example.com/bad"),
        ]
    )
    news = collect_news_from_news_api_org({"search_queries": ["q"]})["news"]
    assert [a.url for a in news] == ["https://example.com/ok"]


def test_news_api_failure_returns_empty_list(monkeypatch):
    def boom(self, queries):
        raise RuntimeError("API down")

    monkeypatch.setattr(api.NewsApiSearch, "get_news", boom)
    assert collect_news_from_news_api_org({"search_queries": ["q"]}) == {"news": []}


def test_currents_duplicates_are_removed(monkeypatch):
    raw = {
        "id": "abc",
        "title": "Same story",
        "description": "Body",
        "published": "2025-01-01 10:00:00 +0000",
        "url": "https://example.com/same",
    }
    monkeypatch.setattr(
        api.CurrentNewsApiSearch, "get_ai_news", lambda self: {"data": [raw, dict(raw)]}
    )
    news = collect_news_from_current_news_api({})["news"]
    assert len(news) == 1


def test_mock_mode_collects_from_bundled_data(mock_mode):
    news_api = collect_news_from_news_api_org({"search_queries": ["q"]})["news"]
    currents = collect_news_from_current_news_api({})["news"]

    assert news_api and currents
    currents_urls = [a.url for a in currents]
    assert len(currents_urls) == len(set(currents_urls))
