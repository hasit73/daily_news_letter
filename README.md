# Daily AI Newsletter Agent 🤖📰

[![CI](https://github.com/hasit73/daily_news_letter/actions/workflows/ci.yml/badge.svg)](https://github.com/hasit73/daily_news_letter/actions/workflows/ci.yml)

A LangGraph multi-agent pipeline that collects the latest AI, technology and India news from multiple sources, rewrites it with Google Gemini for readability, and delivers it as a daily digest to WhatsApp.

## 🌟 Overview

This project leverages **LangGraph** to create a sophisticated multi-agent workflow that:

- 🔍 Intelligently searches for the latest AI and technology news
- 🧹 Sanitizes and processes news content
- ✨ Enriches articles using AI for better readability
- 📱 Formats and delivers the newsletter via WhatsApp

## 🚀 Key Features

- **Multi-Source News Aggregation**: Fetches news from NewsAPI.org and CurrentsAPI
- **AI-Powered Content Enhancement**: Uses Google Gemini to improve article quality and readability
- **Content Filtering**: Dedupes stories across sources and keeps the most recent articles
- **WhatsApp Integration**: Delivers formatted newsletters directly to your phone
- **Workflow Orchestration**: Built with LangGraph for robust agent coordination
- **Parallel Execution**: News sources are queried concurrently and enrichment runs in parallel batches
- **Mock Data Support**: Bundled API responses for development without news API keys

## 🏗️ Architecture

The system uses a **multi-agent architecture** with the following components:

```
Search Query Builder → News Collector ─┬─ NewsAPI.org ─┬→ Aggregator → Sanitizer → Selector
                                       └─ CurrentsAPI ─┘
  → Enricher (parallel batches) → WhatsApp Formatter → Delivery
```

Here is detailed **[architecture](docs/architecture.md)**.

### Core Agents

- **Search Query Builder**: Generates targeted search queries for AI/tech news
- **News Collector**: Fetches articles from multiple news APIs
- **News Sanitizer**: Cleans and normalizes article content
- **News Selector**: Filters and selects the most relevant articles
- **News Enricher**: Uses AI to improve headlines and content quality
- **Message Formatter**: Formats articles for WhatsApp delivery

## 📋 Prerequisites

- Python 3.10+
- WhatsApp Cloud API access (Meta developer account)
- News API keys (NewsAPI.org, CurrentsAPI)
- Google Gemini API key

## 🛠️ Quick Start

1. **Clone and install**

   ```bash
   git clone https://github.com/hasit73/daily_news_letter.git
   cd daily_news_letter
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   ```

2. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the newsletter**
   ```bash
   daily-news-letter
   # or: python -m daily_news_letter.run
   ```

## 🔧 Configuration

Key environment variables:

```env
# News APIs
NEWS_API_ORG=your_newsapi_key
CURRENT_API_SERVICES=your_currentsapi_key

# Google Gemini
GOOGLE_API_KEY=your_gemini_key

# WhatsApp Business API
WHATSAPP_API_ACCESS_TOKEN=your_whatsapp_token
WHATSAPP_SENDER_ACCOUNT_ID=your_app_account_id
WHATSAPP_RECIPIENT_NUMBER=recipient_phone_number

# Development
USE_MOCK_DATA=false
```

## 🧪 Development

```bash
pip install -e ".[dev]"
pytest              # offline test suite, no API keys needed
ruff check .        # lint
ruff format .       # format
```

The tests replace Gemini with a fake LLM and run against the bundled mock API responses, so they
need no network access. CI runs lint and tests on Python 3.10–3.12 for every push and pull request.

To try the pipeline without news API keys, set `USE_MOCK_DATA=true`. This uses the bundled
responses in `src/daily_news_letter/mocks/data/` and skips the search-query LLM call. Enrichment
still uses Gemini, and the result is still sent to WhatsApp.

## 📁 Project Structure

```
src/daily_news_letter/
├── workflow.py          # LangGraph graph definition
├── run.py               # Entry point: run graph, send messages
├── agents/              # One module per graph node
├── api.py               # NewsAPI, Currents and WhatsApp clients
├── llm.py               # Gemini client
├── models.py            # Pydantic models and graph state
├── prompts.py           # LLM prompts and message template
├── common.py            # Config, sanitization and date helpers
└── mocks/               # Mock API responses for development
tests/                   # pytest suite
docs/architecture.md     # Detailed design notes
```

## 🗺️ Roadmap

Planned work is tracked in [GitHub Issues](https://github.com/hasit73/daily_news_letter/issues):

- Retries with backoff for LLM and news API calls ([#1](https://github.com/hasit73/daily_news_letter/issues/1))
- Structured logging instead of `print` ([#2](https://github.com/hasit73/daily_news_letter/issues/2))
- Remember previously sent stories so they aren't repeated on later days ([#3](https://github.com/hasit73/daily_news_letter/issues/3))
- Configurable interests and sources instead of hard-coded prompts ([#4](https://github.com/hasit73/daily_news_letter/issues/4))
- Additional delivery channels (email, Telegram) ([#5](https://github.com/hasit73/daily_news_letter/issues/5))
- Built-in scheduling and a Docker image for deployment ([#6](https://github.com/hasit73/daily_news_letter/issues/6))
- Dry-run mode that prints the newsletter instead of sending it ([#7](https://github.com/hasit73/daily_news_letter/issues/7))

## 🙏 Acknowledgments

- **LangGraph** - For the powerful agent orchestration framework
- **Google Gemini** - For AI-powered content enhancement
- **NewsAPI.org & CurrentsAPI** - For reliable news data sources
- **WhatsApp Business API** - For seamless message delivery

---

**Built with ❤️ using LangGraph and AI**
