# Daily AI Newsletter Agent 🤖📰

An intelligent AI-powered system that automatically generates and delivers personalized daily newsletters focused on AI and technology trends directly to your WhatsApp.

## 🌟 Overview

This project leverages **LangGraph** to create a sophisticated multi-agent workflow that:

- 🔍 Intelligently searches for the latest AI and technology news
- 🧹 Sanitizes and processes news content
- ✨ Enriches articles using AI for better readability
- 📱 Formats and delivers personalized newsletters via WhatsApp

## 🚀 Key Features

- **Multi-Source News Aggregation**: Fetches news from NewsAPI.org and CurrentsAPI
- **AI-Powered Content Enhancement**: Uses Google Gemini to improve article quality and readability
- **Smart Content Filtering**: Automatically selects the most relevant and recent articles
- **WhatsApp Integration**: Delivers formatted newsletters directly to your phone
- **Workflow Orchestration**: Built with LangGraph for robust agent coordination
- **Mock Data Support**: Development-friendly with mock data capabilities

## 🏗️ Architecture

The system uses a **multi-agent architecture** with the following components:

```
Search Query Builder → News Collector → News Aggregator →
Sanitizer → Selector → Enricher → WhatsApp Formatter → Delivery
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
- WhatsApp Business API access
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

## 🎯 Use Cases

- **Daily AI Updates**: Stay informed about the latest AI breakthroughs
- **Technology Trends**: Get curated tech news delivered automatically
- **Personal News Assistant**: Receive personalized newsletters on your schedule
- **Research Tool**: Automated content aggregation for AI researchers

## 🙏 Acknowledgments

- **LangGraph** - For the powerful agent orchestration framework
- **Google Gemini** - For AI-powered content enhancement
- **NewsAPI.org & CurrentsAPI** - For reliable news data sources
- **WhatsApp Business API** - For seamless message delivery

---

**Built with ❤️ using LangGraph and AI**
