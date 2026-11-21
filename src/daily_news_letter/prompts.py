WHATSAPP_MESSAGE_FORMAT = """
*{{ headline }}* {% if sub_headline %}- {{ sub_headline }}{% endif %}
{{ content }}\n
🔗 Read more - {{url}}\n
_Published at : {{published_at}}_"""

NEWS_ENRICHMENT_PROMPT = """
You are a news content writer. Improve a list of news articles (headline, optional sub_headline, content, URL, date) to be engaging and reader-friendly.

Instructions:
1. Revise headline, sub_headline, and content using clear, simple language without changing meaning.
2. Don't update/remove fields other than headline, sub_headline, and content.
3. Assign one relevant 'category' per article (e.g., 'Technology', 'Crime') based on headline/subheadline.
4. You may use emojis sparingly to enhance appeal.
5. Keep the number of articles the same as input; return all articles, even if unchanged.
6. Output only the articles in JSON, each inside <NewsArticle></NewsArticle> tags.
7. Final revised list of news article must be sorted on date field in descending manner where recent news should be at top.

Goal: Make articles appealing and add a category.
"""

SEARCH_QUERY_BUILDER_PROMPT = """
<Goal>
I want to stay updated on the latest technology trends, artificial intelligence (AI) news, and current events in India. I need a list of highly effective search queries that will help me discover top, trending, and relevant articles across these topics.

<Interest>
Generate a list of search queries focusing on:

1. Emerging and trending technology news
2. Recent breakthroughs or developments in AI
3. Innovative or unusual applications of AI
4. Challenges, risks, or controversies in AI
5. Major current events and top news in India

<Rules>
- Provide at least 5 distinct search queries
- Queries must be specific, current-focused, and usable in search engines or news aggregators
- Avoid vague or generic phrasing (e.g., “tech news”)
- Ensure each query targets a different angle or subtopic — no overlaps
- Avoid domain-specific queries (like AI in healthcare, etc.)
- Keep queries clear, concise, and effective
- Don't mention date or year, instead use keywords like latest and recent.
"""
