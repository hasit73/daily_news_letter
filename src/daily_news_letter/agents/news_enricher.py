from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Send

from daily_news_letter.common import Nodes
from daily_news_letter.llm import get_llm
from daily_news_letter.models import NewsExtractorState, OutputEnrichedNewsArticleList
from daily_news_letter.prompts import NEWS_ENRICHMENT_PROMPT


def enrich_news_router(state: NewsExtractorState):
    """Split selected news into batches and fan them out to parallel enricher nodes."""
    news = state["sanitized_news"]
    BATCH_SIZE = 5
    batches = []
    for batch_start_index in range(0, len(news), BATCH_SIZE):
        batches.append(
            Send(
                Nodes.NEWS_ENRICHER,
                {"news_batch": news[batch_start_index : batch_start_index + BATCH_SIZE]},
            )
        )
    return batches


def news_enricher(state: NewsExtractorState):
    """Rewrite one batch of articles with the LLM and assign each a category."""
    news_batch = state["news_batch"]
    news_list_str = "\n".join([news_article.model_dump_json() for news_article in news_batch])
    news_articles = f"""News List : \n{news_list_str}"""

    structured_llm = get_llm().with_structured_output(OutputEnrichedNewsArticleList)
    response = structured_llm.invoke(
        [
            SystemMessage(NEWS_ENRICHMENT_PROMPT),
            HumanMessage(f"Here is list of news articles:\n {news_articles}"),
        ]
    )
    print("Created a message with total new articles : ", len(response.enriched_news))
    return {"enriched_news": response.enriched_news}
