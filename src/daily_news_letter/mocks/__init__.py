import json
import os

MOCK_DIR_PATH = os.path.dirname(os.path.abspath(__file__))


def _load_mock_file(filename):
    file_path = os.path.join(MOCK_DIR_PATH, "data", filename)
    # Ensure path is within the expected directory
    if not file_path.startswith(os.path.join(MOCK_DIR_PATH, "data")):
        raise ValueError("Invalid file path")
    with open(file_path) as f:
        return json.load(f)


MOCK_NEWS_API_RESPONSE = _load_mock_file("news_api_response.json")
MOCK_CURRENT_API_RESPONSE = _load_mock_file("current_api_response.json")
MOCK_SEARCH_QUERIES = [
    "latest technology trends",
    "recent AI breakthroughs",
    "innovative applications of AI",
    "AI challenges risks and controversies",
    "top news India",
]
