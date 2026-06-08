from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# @tool
# def web_search(query: str) -> str:
#     """Searches the web for the given query. Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets"""
#     results=tavily.search(query=query,max_results=5)

#     out= []
#     for r in results['results']:
#         out.append(
#             f"Title:{r['title']}\nURL:{r['url']}\nSnippet:{r['snippet'][:300]}"
#         )
#     return "\n".join(out)

from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """
    Searches the web for the given query.
    Returns titles, URLs, and snippets from search results.
    """

    try:
        results = tavily.search(query=query, max_results=5)

        out = []

        for r in results.get("results", []):

            snippet = (
                r.get("snippet")
                or r.get("content")
                or r.get("raw_content")
                or "No snippet available"
            )

            title = r.get("title", "No title")
            url = r.get("url", "No URL")

            out.append(
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Snippet: {snippet[:300]}"
            )

        return "\n\n".join(out)

    except Exception as e:
        return f"Web search error: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

        