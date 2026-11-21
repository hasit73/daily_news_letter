from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated, TypedDict
import operator


class SearchQueries(BaseModel):
    search_queries: List[str]


class NewsArticle(BaseModel):
    headline: str
    sub_headline: Optional[str] = None
    content: str
    metadata: Optional[Dict[str, Any]] = {}
    url: Optional[str] = None
    published_at: str
    author: Optional[str] = None


class EnrichedNewsArticle(NewsArticle):
    category: str


class NewsCollectorResult(BaseModel):
    news: List[NewsArticle]


class OutputEnrichedNewsArticleList(BaseModel):
    enriched_news: Annotated[List[EnrichedNewsArticle], operator.add]


# Graph states
class NewsAggregationState(TypedDict):
    news: Annotated[List[NewsArticle], operator.add]
    search_queries: SearchQueries


class NewsExtractorState(TypedDict):
    search_queries: SearchQueries
    news: Annotated[List[NewsArticle], operator.add]
    sanitized_news: List[NewsArticle]
    enriched_news: Annotated[List[EnrichedNewsArticle], operator.add]
    output_messages: List[str]
    formatted_news: Annotated[List[str], operator.add]
