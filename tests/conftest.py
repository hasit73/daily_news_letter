import importlib
import json

import pytest

from daily_news_letter.models import (
    EnrichedNewsArticle,
    NewsArticle,
    OutputEnrichedNewsArticleList,
)

ENV_VARS = (
    "USE_MOCK_DATA",
    "GOOGLE_API_KEY",
    "NEWS_API_ORG",
    "CURRENT_API_SERVICES",
    "WHATSAPP_API_ACCESS_TOKEN",
    "WHATSAPP_SENDER_ACCOUNT_ID",
    "WHATSAPP_RECIPIENT_NUMBER",
)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Isolate tests from any real keys in the developer's shell or .env."""
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def mock_mode(monkeypatch):
    monkeypatch.setenv("USE_MOCK_DATA", "true")


class _FakeStructuredLLM:
    """Echoes the input articles back as EnrichedNewsArticle with a category."""

    def __init__(self, calls):
        self.calls = calls

    def invoke(self, messages):
        self.calls.append(messages)
        articles = [
            json.loads(line) for line in messages[-1].content.splitlines() if line.startswith("{")
        ]
        return OutputEnrichedNewsArticleList(
            enriched_news=[EnrichedNewsArticle(**a, category="Tech") for a in articles]
        )


class FakeLLM:
    def __init__(self):
        self.calls = []

    def with_structured_output(self, _schema):
        return _FakeStructuredLLM(self.calls)


@pytest.fixture
def fake_llm(monkeypatch):
    llm = FakeLLM()
    # agents/__init__ re-exports functions that shadow same-named submodules,
    # so resolve the module objects explicitly.
    for module in (
        "daily_news_letter.agents.news_enricher",
        "daily_news_letter.agents.search_query_builder",
    ):
        monkeypatch.setattr(importlib.import_module(module), "get_llm", lambda: llm)
    return llm


def make_article(**overrides) -> NewsArticle:
    fields = {
        "headline": "Headline",
        "content": "Some content",
        "url": "https://example.com/a",
        "published_at": "2025-01-01T00:00:00+00:00",
    }
    fields.update(overrides)
    return NewsArticle(**fields)


def make_enriched(**overrides) -> EnrichedNewsArticle:
    return EnrichedNewsArticle(**make_article(**overrides).model_dump(), category="Tech")
