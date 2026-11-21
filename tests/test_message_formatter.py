from conftest import make_enriched

from daily_news_letter.agents.message_formatter import format_whatsapp_messages
from daily_news_letter.common import MAX_MESSAGE_CHAR_LIMIT, MESSAGE_SEPARATOR


def _format(articles):
    return format_whatsapp_messages({"enriched_news": articles})["output_messages"]


def test_empty_input_produces_no_messages():
    assert _format([]) == []


def test_every_article_is_delivered_when_messages_overflow():
    articles = [
        make_enriched(headline=f"Story {i}", content="x" * 1500, url=f"https://e.com/{i}")
        for i in range(7)
    ]
    messages = _format(articles)

    assert len(messages) > 1
    delivered = [part for message in messages for part in message]
    assert len(delivered) == len(articles)
    for i in range(7):
        assert sum(f"*Story {i}*" in part for part in delivered) == 1


def test_messages_respect_whatsapp_limit_including_separators():
    articles = [make_enriched(content="y" * 1000, url=f"https://e.com/{i}") for i in range(12)]
    for message in _format(articles):
        assert len(MESSAGE_SEPARATOR.join(message)) <= MAX_MESSAGE_CHAR_LIMIT


def test_oversized_article_is_truncated_not_dropped():
    messages = _format([make_enriched(content="z" * (MAX_MESSAGE_CHAR_LIMIT * 2))])

    assert len(messages) == 1 and len(messages[0]) == 1
    assert len(messages[0][0]) <= MAX_MESSAGE_CHAR_LIMIT
    assert "…" in messages[0][0]


def test_plain_text_is_not_html_escaped():
    [[text]] = _format([make_enriched(headline="R&D <update>", content="AT&T's \"plan\"")])
    assert "R&D <update>" in text
    assert "AT&T's \"plan\"" in text
    assert "&amp;" not in text


def test_message_includes_link_and_optional_sub_headline():
    [[with_sub]] = _format([make_enriched(sub_headline="Subtitle")])
    [[without_sub]] = _format([make_enriched(sub_headline=None)])

    assert "- Subtitle" in with_sub
    assert "None" not in without_sub
    assert "🔗 Read more - https://example.com/a" in with_sub
