import re

from daily_news_letter.agents.news_selector import MAX_SELECTED_NEWS
from daily_news_letter.workflow import create_workflow


def _run():
    return create_workflow().invoke({}, config={"configurable": {"thread_id": "test"}})


def test_full_pipeline_in_mock_mode(mock_mode, fake_llm):
    result = _run()

    # Collectors' results are merged once, not duplicated by the aggregator.
    urls = [a.url for a in result["news"]]
    assert len(urls) == len(set(urls))

    selected = result["sanitized_news"]
    assert 0 < len(selected) <= MAX_SELECTED_NEWS
    assert len(result["enriched_news"]) == len(selected)

    delivered = [part for message in result["output_messages"] for part in message]
    assert len(delivered) == len(selected)

    text = "\n".join(delivered)
    assert not re.search(r"</?[a-z]+[^>]*>", text), "HTML leaked into WhatsApp text"
    assert "&amp;" not in text


def test_mock_mode_does_not_call_llm_for_search_queries(mock_mode, fake_llm):
    _run()
    system_prompts = [messages[0].content for messages in fake_llm.calls]
    assert all("search queries" not in prompt for prompt in system_prompts)


def test_enricher_batches_articles(mock_mode, fake_llm):
    result = _run()
    batches = len(fake_llm.calls)
    assert batches == -(-len(result["sanitized_news"]) // 5)
