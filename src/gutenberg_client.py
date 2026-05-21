"""Project Gutenberg client for searching and downloading classic books."""

import requests
import re
from typing import List, Dict, Optional
from src.utils import rate_limit


# Gutendex API - a modern REST API for Project Gutenberg
GUTENDEX_URL = "https://gutendex.com/books"


def search_books(query: str, topic: str = "", max_results: int = 20) -> List[Dict]:
    """Search Project Gutenberg via Gutendex API.

    Returns list of book metadata dicts.
    """
    params = {
        "search": query,
        "languages": "en",
        "mime_type": "text/plain",
    }
    if topic:
        params["topic"] = topic

    try:
        rate_limit(1.0)
        resp = requests.get(GUTENDEX_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[Gutenberg] Search failed for '{query}': {e}")
        return []

    books = []
    for item in data.get("results", [])[:max_results]:
        authors = item.get("authors", [])
        author_name = authors[0].get("name", "") if authors else ""

        # Find plain text download URL
        text_url = None
        for fmt, url in item.get("formats", {}).items():
            if "text/plain" in fmt and url.endswith(".txt"):
                text_url = url
                break
            elif "text/plain" in fmt:
                text_url = url

        subjects = item.get("subjects", [])

        book = {
            "title": item.get("title", ""),
            "author": author_name,
            "isbn": "",
            "publication_year": "",
            "gutenberg_id": str(item.get("id", "")),
            "text_url": text_url,
            "subjects": subjects,
            "download_count": item.get("download_count", 0),
            "source": "gutenberg",
        }
        books.append(book)

    return books


def search_by_category(category_name: str, keywords: List[str],
                        limit_per_query: int = 10) -> List[Dict]:
    """Search Gutenberg across keywords for a category."""
    all_books = []

    for kw in keywords:
        results = search_books(kw, topic=kw, max_results=limit_per_query)
        for b in results:
            b["category"] = category_name
        all_books.extend(results)

    return all_books


def download_book_text(text_url: str) -> Optional[str]:
    """Download full text from Project Gutenberg."""
    if not text_url:
        return None
    try:
        rate_limit(1.0)
        resp = requests.get(text_url, timeout=60)
        resp.raise_for_status()
        text = resp.text

        # Strip Gutenberg header/footer
        text = strip_gutenberg_boilerplate(text)

        if len(text) > 1000:
            return text
        return None
    except Exception as e:
        print(f"[Gutenberg] Download failed for {text_url}: {e}")
        return None


def download_by_id(gutenberg_id: str) -> Optional[str]:
    """Download book text by Gutenberg ID."""
    if not gutenberg_id:
        return None
    # Try common URL patterns
    urls = [
        f"https://www.gutenberg.org/cache/epub/{gutenberg_id}/pg{gutenberg_id}.txt",
        f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt",
        f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}.txt",
    ]
    for url in urls:
        text = download_book_text(url)
        if text:
            return text
    return None


def strip_gutenberg_boilerplate(text: str) -> str:
    """Remove Project Gutenberg header and footer boilerplate."""
    # Find start of actual content
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG",
        r"START OF (THE|THIS) PROJECT GUTENBERG",
    ]
    for marker in start_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            # Skip to next line after marker
            idx = text.find('\n', match.end())
            if idx != -1:
                text = text[idx + 1:]
            break

    # Find end of actual content
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG",
        r"END OF (THE|THIS) PROJECT GUTENBERG",
    ]
    for marker in end_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            text = text[:match.start()]
            break

    return text.strip()
