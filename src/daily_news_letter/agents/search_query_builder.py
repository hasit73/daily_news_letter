import os
from daily_news_letter.models import NewsExtractorState, SearchQueries
from langchain_core.messages import SystemMessage, HumanMessage
from daily_news_letter.llm import gemini_llm
from daily_news_letter.prompts import SEARCH_QUERY_BUILDER_PROMPT
from daily_news_letter.mocks import MOCK_SEARCH_QUERIES
from daily_news_letter import common


def search_query_builder(state: NewsExtractorState) -> NewsExtractorState:

    structured_output_llm = gemini_llm.with_structured_output(SearchQueries)
    response = structured_output_llm.invoke(
        [
            SystemMessage(SEARCH_QUERY_BUILDER_PROMPT),
            HumanMessage("Generate list of search queries"),
        ]
    )
    if common.USE_MOCK_DATA:
        return {"search_queries": MOCK_SEARCH_QUERIES}
    return {"search_queries": response.search_queries}
