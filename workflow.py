from langgraph.graph import StateGraph, START, END

from daily_news_letter import agents
from daily_news_letter.models import NewsExtractorState
from daily_news_letter.common import Nodes
from langgraph.checkpoint.memory import MemorySaver


def create_workflow():
    memory = MemorySaver()
    builder = StateGraph(NewsExtractorState)

    builder.set_entry_point(Nodes.SEARCH_QUERY_BUILDER)
    builder.add_node(Nodes.SEARCH_QUERY_BUILDER, agents.search_query_builder)

    # News aggregator nodes and edges
    builder.add_node(Nodes.COLLECT_NEWS, agents.collect_news)
    builder.add_node(
        Nodes.COLLECT_NEWS_FROM_NEWS_API_ORG, agents.collect_news_from_news_api_org
    )
    builder.add_node(
        Nodes.COLLECT_NEWS_FROM_CURRENT_NEWS_API,
        agents.collect_news_from_current_news_api,
    )
    builder.add_node(Nodes.NEWS_AGGREGATOR, agents.news_aggregator)
    builder.add_node(Nodes.SANITIZE_NEWS, agents.sanitize_news)
    builder.add_node(Nodes.NEWS_SELECTOR, agents.news_selector)
    builder.add_node(Nodes.NEWS_ENRICHER, agents.news_enricher)
    builder.add_node(Nodes.FORMAT_WHATSAPP_MESSAGES, agents.format_whatsapp_messages)

    builder.add_edge(Nodes.SEARCH_QUERY_BUILDER, Nodes.COLLECT_NEWS)
    builder.add_edge(Nodes.COLLECT_NEWS, Nodes.COLLECT_NEWS_FROM_NEWS_API_ORG)
    builder.add_edge(Nodes.COLLECT_NEWS, Nodes.COLLECT_NEWS_FROM_CURRENT_NEWS_API)

    builder.add_edge(Nodes.COLLECT_NEWS_FROM_NEWS_API_ORG, Nodes.NEWS_AGGREGATOR)
    builder.add_edge(Nodes.COLLECT_NEWS_FROM_CURRENT_NEWS_API, Nodes.NEWS_AGGREGATOR)
    builder.add_edge(Nodes.NEWS_AGGREGATOR, Nodes.SANITIZE_NEWS)
    builder.add_edge(Nodes.SANITIZE_NEWS, Nodes.NEWS_SELECTOR)
    builder.add_conditional_edges(
        Nodes.NEWS_SELECTOR, agents.enrich_news_router, [Nodes.NEWS_ENRICHER]
    )
    builder.add_edge(Nodes.NEWS_ENRICHER, Nodes.FORMAT_WHATSAPP_MESSAGES)
    builder.add_edge(Nodes.FORMAT_WHATSAPP_MESSAGES, END)

    graph = builder.compile(checkpointer=memory)
    return graph
