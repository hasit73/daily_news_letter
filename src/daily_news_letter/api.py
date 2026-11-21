from typing import List

from datetime import datetime, timezone, timedelta
import requests
import os
from datetime import timezone
from daily_news_letter.mocks import MOCK_CURRENT_API_RESPONSE, MOCK_NEWS_API_RESPONSE
from daily_news_letter import common


class NewsApiSearch:
    BASE_URL = "https://newsapi.org/v2/{endpoint}?q={search_query}&pageSize={page_size}&searchIn=title,description&from={from_datetime}"

    def __init__(self):
        pass

    def build_search_query(self, search_queries: List[str]):
        return " OR ".join([" OR ".join(query.split()) for query in search_queries])

    @property
    def from_datetime(self):
        return (
            (datetime.now() - timedelta(days=7))
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    def get_news(
        self,
        queries: List[str],
        page_size: int = 5,
    ):
        search_query = self.build_search_query(queries)
        url = NewsApiSearch.BASE_URL.format(
            endpoint="everything",
            search_query=search_query,
            page_size=page_size,
            from_datetime=self.from_datetime,
        )
        if common.USE_MOCK_DATA:
            return MOCK_NEWS_API_RESPONSE
        print("📰 Fetching news from ", url)
        response = requests.get(url, headers={"X-Api-Key": os.getenv("NEWS_API_ORG")})
        response_json = response.json()
        return {
            "data": response_json.get("articles"),
            "count": response_json.get("totalResults"),
        }


class CurrentNewsApiSearch:
    BASE_URL = "https://api.currentsapi.services/v1/search?keywords={search_query}&page_size={page_size}&limit={page_size}&start_date={from_datetime}"

    def __init__(self):
        pass

    @property
    def from_datetime(self):
        return (
            (datetime.now() - timedelta(days=7))
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    def get_news(
        self,
        search_query: str,
        page_size: int = 5,
    ):
        url = CurrentNewsApiSearch.BASE_URL.format(
            search_query=search_query,
            page_size=page_size,
            from_datetime=self.from_datetime,
        )
        if common.USE_MOCK_DATA:
            return MOCK_CURRENT_API_RESPONSE
        print("📰 Fetching news from ", url)
        response = requests.get(
            url, headers={"Authorization": os.getenv("CURRENT_API_SERVICES")}
        )
        response_json = response.json()
        return {
            "data": response_json.get("news"),
            "count": len(response_json.get("news")),
        }

    def get_ai_news(self):
        queries = ["ai development", "ai controversy"]
        results = {"data": []}
        for query in queries:
            data = self.get_news(query)
            results["data"] += data.get("data", [])
        results["count"] = len(results["data"])
        return results

    def get_latest_news(self):
        url = "https://api.currentsapi.services/v1/latest-news"
        if common.USE_MOCK_DATA:
            return MOCK_CURRENT_API_RESPONSE
        print("📰 Fetching latest news from ", url)
        response = requests.get(
            url, headers={"Authorization": os.getenv("CURRENT_API_SERVICES")}
        )
        response_json = response.json()
        return {
            "data": response_json.get("news"),
            "count": len(response_json.get("news")),
        }


def send_message(message: str):
    resp = requests.post(
        f"https://graph.facebook.com/v22.0/{os.getenv('WHATSAPP_SENDER_ACCOUNT_ID')}/messages?access_token="
        + os.environ.get("WHATSAPP_API_ACCESS_TOKEN"),
        json={
            "messaging_product": "whatsapp",
            "to": os.getenv("WHATSAPP_RECIPIENT_NUMBER"),
            "type": "text",
            "text": {"body": message, "preview_url": False},
        },
    )
    return resp
