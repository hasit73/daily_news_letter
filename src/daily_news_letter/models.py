import operator
from typing import Annotated, Any, TypedDict

from pydantic import BaseModel


class SearchQueries(BaseModel):
    search_queries: list[str]


class NewsArticle(BaseModel):
    headline: str
    sub_headline: str | None = None
    content: str
    metadata: dict[str, Any] | None = {}
    url: str | None = None
    published_at: str
    author: str | None = None


class EnrichedNewsArticle(NewsArticle):
    category: str


class NewsCollectorResult(BaseModel):
    news: list[NewsArticle]


class OutputEnrichedNewsArticleList(BaseModel):
    enriched_news: Annotated[list[EnrichedNewsArticle], operator.add]


# Graph states
class NewsAggregationState(TypedDict):
    news: Annotated[list[NewsArticle], operator.add]
    search_queries: SearchQueries


class NewsExtractorState(TypedDict):
    search_queries: SearchQueries
    news: Annotated[list[NewsArticle], operator.add]
    sanitized_news: list[NewsArticle]
    enriched_news: Annotated[list[EnrichedNewsArticle], operator.add]
    output_messages: list[list[str]]
    formatted_news: Annotated[list[str], operator.add]
