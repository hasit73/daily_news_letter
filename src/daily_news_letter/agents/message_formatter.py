from jinja2 import Template
from daily_news_letter.models import NewsExtractorState
from daily_news_letter.common import MAX_MESSAGE_CHAR_LIMIT
from daily_news_letter.prompts import WHATSAPP_MESSAGE_FORMAT


def format_whatsapp_messages(state: NewsExtractorState):
    """Format enriched news in terms of whatsapp messages. ensures each message size doesn't exceed whatsapp message size limit."""
    enriched_news = state["enriched_news"]
    output_messages = []
    temp_message_list = []
    message_size = 0

    template = Template(WHATSAPP_MESSAGE_FORMAT, autoescape=True)

    for article in enriched_news:
        formatted_message = template.render(
            headline=article.headline,
            sub_headline=article.sub_headline,
            content=article.content,
            published_at=article.published_at,
            url=article.url,
        ).strip()
        article_size = len(formatted_message)
        if message_size + article_size <= MAX_MESSAGE_CHAR_LIMIT:
            temp_message_list.append(formatted_message)
            message_size += article_size
        else:
            output_messages.append(temp_message_list)
            temp_message_list = []
            message_size = 0
    if temp_message_list:
        output_messages.append(temp_message_list)
    return {"output_messages": output_messages}
