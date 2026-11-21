import pytest
import requests

from daily_news_letter import api


def test_build_search_query_ands_words_and_ors_queries():
    query = api.NewsApiSearch.build_search_query(["recent AI breakthroughs", "top news", ""])
    assert query == "(recent AND AI AND breakthroughs) OR (top AND news)"


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.ok = True

    def json(self):
        return self._payload

    def raise_for_status(self):
        pass


def test_news_api_sends_key_header_and_params(monkeypatch):
    monkeypatch.setenv("NEWS_API_ORG", "secret-key")
    captured = {}

    def fake_get(url, params, headers, timeout):
        captured.update(url=url, params=params, headers=headers, timeout=timeout)
        return _FakeResponse({"articles": None, "totalResults": 0})

    monkeypatch.setattr(requests, "get", fake_get)
    result = api.NewsApiSearch().get_news(["ai news"])

    assert result == {"data": [], "count": 0}
    assert captured["headers"] == {"X-Api-Key": "secret-key"}
    assert captured["params"]["q"] == "(ai AND news)"
    assert "secret-key" not in captured["url"]
    assert captured["timeout"]


def test_currents_handles_missing_news_field(monkeypatch):
    monkeypatch.setenv("CURRENT_API_SERVICES", "key")
    monkeypatch.setattr(requests, "get", lambda *a, **kw: _FakeResponse({"status": "ok"}))
    assert api.CurrentNewsApiSearch().get_news("ai") == {"data": [], "count": 0}


def test_news_api_missing_key_raises_clear_error():
    with pytest.raises(RuntimeError, match="NEWS_API_ORG"):
        api.NewsApiSearch().get_news(["ai"])


def test_mock_mode_makes_no_http_calls(monkeypatch, mock_mode):
    def no_network(*args, **kwargs):
        raise AssertionError("network call in mock mode")

    monkeypatch.setattr(requests, "get", no_network)
    assert api.NewsApiSearch().get_news(["ai"])["data"]
    assert api.CurrentNewsApiSearch().get_ai_news()["data"]


def test_send_message_puts_token_in_header_not_url(monkeypatch):
    monkeypatch.setenv("WHATSAPP_API_ACCESS_TOKEN", "tok123")
    monkeypatch.setenv("WHATSAPP_SENDER_ACCOUNT_ID", "555")
    monkeypatch.setenv("WHATSAPP_RECIPIENT_NUMBER", "+910000000000")
    captured = {}

    def fake_post(url, headers, json, timeout):
        captured.update(url=url, headers=headers, json=json)
        return _FakeResponse({})

    monkeypatch.setattr(requests, "post", fake_post)
    api.send_message("hello")

    assert captured["url"] == "https://graph.facebook.com/v22.0/555/messages"
    assert "tok123" not in captured["url"]
    assert captured["headers"]["Authorization"] == "Bearer tok123"
    assert captured["json"]["to"] == "+910000000000"
    assert captured["json"]["text"]["body"] == "hello"


def test_send_message_missing_config_raises():
    with pytest.raises(RuntimeError, match="WHATSAPP_SENDER_ACCOUNT_ID"):
        api.send_message("hello")
