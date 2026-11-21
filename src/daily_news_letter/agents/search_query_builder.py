from langchain_core.messages import HumanMessage, SystemMessage

from daily_news_letter import common
from daily_news_letter.llm import get_llm
from daily_news_letter.mocks import MOCK_SEARCH_QUERIES
from daily_news_letter.models import NewsExtractorState, SearchQueries
from daily_news_letter.prompts import SEARCH_QUERY_BUILDER_PROMPT


def search_query_builder(state: NewsExtractorState) -> NewsExtractorState:
    """Ask the LLM for a set of targeted news search queries."""
    if common.use_mock_data():
        return {"search_queries": MOCK_SEARCH_QUERIES}

    structured_output_llm = get_llm().with_structured_output(SearchQueries)
    response = structured_output_llm.invoke(
        [
            SystemMessage(SEARCH_QUERY_BUILDER_PROMPT),
            HumanMessage("Generate list of search queries"),
        ]
    )
    return {"search_queries": response.search_queries}
