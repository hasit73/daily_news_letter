from datetime import datetime, timedelta, timezone

import requests

from daily_news_letter import common
from daily_news_letter.mocks import MOCK_CURRENT_API_RESPONSE, MOCK_NEWS_API_RESPONSE

LOOKBACK_DAYS = 7


def _from_datetime() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


class NewsApiSearch:
    BASE_URL = "https://newsapi.org/v2/everything"

    @staticmethod
    def build_search_query(search_queries: list[str]) -> str:
        """Combine queries into one NewsAPI expression: words within a query are
        AND-ed, queries are OR-ed, e.g. (recent AND AI) OR (top AND news)."""
        clauses = []
        for query in search_queries:
            words = query.split()
            if words:
                clauses.append("(" + " AND ".join(words) + ")")
        return " OR ".join(clauses)

    def get_news(self, queries: list[str], page_size: int = 5) -> dict:
        if common.use_mock_data():
            return MOCK_NEWS_API_RESPONSE
        params = {
            "q": self.build_search_query(queries),
            "pageSize": page_size,
            "searchIn": "title,description",
            "from": _from_datetime(),
        }
        print("📰 Fetching news from", self.BASE_URL, params)
        response = requests.get(
            self.BASE_URL,
            params=params,
            headers={"X-Api-Key": common.require_env("NEWS_API_ORG")},
            timeout=common.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        response_json = response.json()
        articles = response_json.get("articles") or []
        return {"data": articles, "count": response_json.get("totalResults", 0)}


class CurrentNewsApiSearch:
    BASE_URL = "https://api.currentsapi.services/v1"
    AI_QUERIES = ("ai development", "ai controversy")

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.BASE_URL}/{endpoint}"
        print("📰 Fetching news from", url, params or "")
        response = requests.get(
            url,
            params=params,
            headers={"Authorization": common.require_env("CURRENT_API_SERVICES")},
            timeout=common.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        news = response.json().get("news") or []
        return {"data": news, "count": len(news)}

    def get_news(self, search_query: str, page_size: int = 5) -> dict:
        if common.use_mock_data():
            return MOCK_CURRENT_API_RESPONSE
        return self._get(
            "search",
            {
                "keywords": search_query,
                "page_size": page_size,
                "start_date": _from_datetime(),
            },
        )

    def get_ai_news(self) -> dict:
        results = []
        for query in self.AI_QUERIES:
            results += self.get_news(query).get("data", [])
        return {"data": results, "count": len(results)}

    def get_latest_news(self) -> dict:
        if common.use_mock_data():
            return MOCK_CURRENT_API_RESPONSE
        return self._get("latest-news")


def send_message(message: str) -> requests.Response:
    """Send a plain-text WhatsApp message via the WhatsApp Cloud API."""
    sender_id = common.require_env("WHATSAPP_SENDER_ACCOUNT_ID")
    return requests.post(
        f"https://graph.facebook.com/v22.0/{sender_id}/messages",
        # Token goes in a header, not the URL, so it never ends up in logs.
        headers={"Authorization": f"Bearer {common.require_env('WHATSAPP_API_ACCESS_TOKEN')}"},
        json={
            "messaging_product": "whatsapp",
            "to": common.require_env("WHATSAPP_RECIPIENT_NUMBER"),
            "type": "text",
            "text": {"body": message, "preview_url": False},
        },
        timeout=common.REQUEST_TIMEOUT_SECONDS,
    )
