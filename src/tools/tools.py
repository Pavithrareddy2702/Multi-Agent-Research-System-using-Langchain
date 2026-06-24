from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient   
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura #dependency need for beautifulsoup
import re

# we can use tavily directly from langchain as well, but here we are using seperately
# to create the custom tavily function

load_dotenv()  


#we have intialized the tavily object here

#example ->
# {
#     'query': 'Latest news on AI Research',
#     'follow_up_questions': None,
#     'answer': None,
#     'images': [],
#     'results': [
#         {
#             'url': 'https://www.artificialintelligence-news.com',
#             'title': 'AI News | Latest News | Insights Powering AI-Driven Business
# Growth',
#             'content': 'IBM Research unveils breakthrough analog AI chip for
# efficient deep learning AI Market Trends August 11, 2023',
#             'score': 0.69968605,
#             'raw_content': None
#         },
    #like these another 4 motre responses
#     ],
#     'response_time': 0.9,
#     'request_id': 'fe48423f-e903-4800-af6b-81846035beef'
# }


tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    results = tavily.search(query=query,max_results=5)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    return "\n----\n".join(out)



@tool

def scrape_url(url: str) -> str:
    """
    Scrape and extract clean readable content from a URL.
    Uses multiple extraction strategies for better reliability.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        # ── Fetch page ─────────────────────────────────────
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        html = response.text

        # ──────────────────────────────────────────────────
        # Strategy 1 → trafilatura (BEST for articles/blogs)
        # ──────────────────────────────────────────────────
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', extracted)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 2 → readability
        # ──────────────────────────────────────────────────
        doc = Document(html)
        clean_html = doc.summary()

        soup = BeautifulSoup(clean_html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if text and len(text.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', text)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 3 → fallback full page extraction
        # ──────────────────────────────────────────────────
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        cleaned = re.sub(r'\s+', ' ', text)

        if cleaned:
            return cleaned[:5000]

        return "Could not extract meaningful content from the page."

    except requests.exceptions.Timeout:
        return "Request timed out while scraping the URL."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    


# # URL Scraper Tool

# The `scrape_url()` tool extracts clean, readable content from a webpage using a multi-layer extraction strategy. It is designed for AI agents, RAG systems, and research workflows where high-quality text extraction is required.

# ### Key Features

# * Downloads webpage content using browser-like request headers.
# * Uses multiple extraction techniques for improved reliability.
# * Removes ads, navigation menus, scripts, footers, and other irrelevant content.
# * Cleans whitespace and formatting issues.
# * Handles timeouts and HTTP errors gracefully.
# * Returns up to 5000 characters of cleaned content.

# ---

# ## Workflow

# ```text
# URL
#  ↓
# Fetch HTML (requests)
#  ↓
# Strategy 1: Trafilatura
#  ↓ Success?
#  Return Content
#  ↓ No
# Strategy 2: Readability + BeautifulSoup
#  ↓ Success?
#  Return Content
#  ↓ No
# Strategy 3: Full Page BeautifulSoup Extraction
#  ↓ Success?
#  Return Content
#  ↓ No
# Return Error Message
# ```

# ---

# ## Strategy 1: Trafilatura Extraction

# The scraper first attempts content extraction using **Trafilatura**, which is highly effective for:

# * News articles
# * Blog posts
# * Documentation pages
# * Research articles

# ```python
# extracted = trafilatura.extract(
#     html,
#     include_comments=False,
#     include_tables=False
# )
# ```

# ### Benefits

# * Removes navigation menus automatically.
# * Excludes comments and user discussions.
# * Extracts the main article body.
# * Produces high-quality text for LLM consumption.

# ---

# ## Strategy 2: Readability Extraction

# If Trafilatura fails, the scraper uses **Readability**.

# ```python
# doc = Document(html)
# clean_html = doc.summary()
# ```

# Readability identifies the main content block of the page and removes:

# * Headers
# * Footers
# * Sidebars
# * Advertisements
# * Navigation menus

# The cleaned HTML is then processed using BeautifulSoup.

# ```python
# soup = BeautifulSoup(clean_html, "html.parser")
# ```

# ---

# ## HTML Cleanup

# Unwanted HTML elements are removed before extracting text.

# ```python
# for tag in soup([
#     "script",
#     "style",
#     "nav",
#     "footer",
#     "header",
#     "aside",
#     "form"
# ]):
#     tag.decompose()
# ```

# ### Removed Elements

# | Tag    | Purpose          |
# | ------ | ---------------- |
# | script | JavaScript code  |
# | style  | CSS styles       |
# | nav    | Navigation menus |
# | footer | Footer content   |
# | header | Header content   |
# | aside  | Sidebar content  |
# | form   | Forms and inputs |

# ---

# ## Text Extraction

# The cleaned HTML is converted into plain text.

# ```python
# text = soup.get_text(
#     separator=" ",
#     strip=True
# )
# ```

# ### Parameters

# * `separator=" "` ensures words remain separated.
# * `strip=True` removes leading and trailing whitespace.

# ---

# ## Text Cleaning

# Multiple spaces, tabs, and line breaks are normalized.

# ```python
# cleaned = re.sub(r'\s+', ' ', text)
# ```

# Example:

# ```text
# Before:
# AI


# is      changing


# the world.

# After:
# AI is changing the world.
# ```

# ---

# ## Strategy 3: Full Page Extraction

# If both Trafilatura and Readability fail, the scraper falls back to direct BeautifulSoup extraction.

# ```python
# soup = BeautifulSoup(html, "html.parser")
# ```

# The same cleanup process is applied, ensuring some usable content can still be extracted even from difficult websites.

# ---

# ## Content Validation

# To avoid returning low-quality results:

# ```python
# if extracted and len(extracted.strip()) > 200:
# ```

# This ensures:

# * Content exists.
# * Content contains meaningful text.
# * Very short or empty pages are ignored.

# ---

# ## Output Limiting

# ```python
# return cleaned[:5000]
# ```

# Only the first 5000 characters are returned to:

# * Reduce token usage.
# * Improve LLM performance.
# * Prevent extremely large webpage outputs.

# ---

# ## Error Handling

# ### Timeout Handling

# ```python
# except requests.exceptions.Timeout:
# ```

# Returns:

# ```text
# Request timed out while scraping the URL.
# ```

# ---

# ### HTTP Errors

# ```python
# except requests.exceptions.HTTPError as e:
# ```

# Examples:

# * 404 Not Found
# * 403 Forbidden
# * 500 Internal Server Error

# Returns:

# ```text
# HTTP error occurred: <error details>
# ```

# ---

# ### Generic Exceptions

# ```python
# except Exception as e:
# ```

# Returns:

# ```text
# Could not scrape URL: <error details>
# ```

# ---

# ## Why Multiple Extraction Strategies?

# Different websites use different HTML structures.

# | Strategy      | Best For                           |
# | ------------- | ---------------------------------- |
# | Trafilatura   | Articles, blogs, documentation     |
# | Readability   | News sites and content-heavy pages |
# | BeautifulSoup | Generic fallback extraction        |

# Using multiple strategies significantly increases extraction success rates across a wide variety of websites.

# ---

# ## Use Cases

# * Research Agents
# * RAG Applications
# * AI Search Systems
# * Content Summarization
# * Knowledge Base Construction
# * Web Data Collection
# * Autonomous AI Agents
