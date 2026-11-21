import pytest

from daily_news_letter.common import (
    normalize_datetime,
    require_env,
    sanitize_html,
    use_mock_data,
)


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        (None, ""),
        ("", ""),
        ("plain text", "plain text"),
        ("<p>AI &amp; ML <strong>rocks</strong></p>", "AI & ML rocks"),
        ('<a href="https://x">link</a> R&amp;D', "link R&D"),
        ("<script>alert(1)</script>safe<style>p{}</style>", "safe"),
        ("<ul><li></li></ul>\r\nline one\r\nline   two", "line one line two"),
        ("Long story… [+3299 chars]", "Long story…"),
    ],
)
def test_sanitize_html_returns_plain_text(html, expected):
    assert sanitize_html(html) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2025-08-10T02:10:00Z", "2025-08-10T02:10:00+00:00"),
        ("2025-08-10 07:40:00 +0530", "2025-08-10T02:10:00+00:00"),
        # Naive timestamps are treated as UTC, not local time.
        ("2025-08-10 02:10:00", "2025-08-10T02:10:00+00:00"),
        ("not a date", ""),
        (None, ""),
    ],
)
def test_normalize_datetime(value, expected):
    assert normalize_datetime(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, False),
        ("false", False),
        ("False", False),
        ("", False),
        ("true", True),
        ("TRUE", True),
        ('"true"', True),
        ("1", True),
        ("yes", True),
    ],
)
def test_use_mock_data(monkeypatch, value, expected):
    if value is not None:
        monkeypatch.setenv("USE_MOCK_DATA", value)
    assert use_mock_data() is expected


def test_require_env(monkeypatch):
    with pytest.raises(RuntimeError, match="NEWS_API_ORG"):
        require_env("NEWS_API_ORG")
    monkeypatch.setenv("NEWS_API_ORG", "key")
    assert require_env("NEWS_API_ORG") == "key"
