"""Google Books API client for searching books and getting metadata/previews."""

import requests
from typing import List, Dict, Optional
from src.utils import rate_limit


# Google Books API (no key required for basic search, but rate-limited)
SEARCH_URL = "https://www.googleapis.com/books/v1/volumes"


def search_books(query: str, subject: str = "", max_results: int = 30) -> List[Dict]:
    """Search Google Books API for books.

    Returns list of book metadata dicts.
    """
    q = query
    if subject:
        q = f"{query}+subject:{subject}"

    params = {
        "q": q,
        "maxResults": min(max_results, 40),
        "langRestrict": "en",
        "printType": "books",
        "orderBy": "relevance",
    }

    try:
        rate_limit(1.0)
        resp = requests.get(SEARCH_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[GoogleBooks] Search failed for '{query}': {e}")
        return []

    books = []
    for item in data.get("items", []):
        vol = item.get("volumeInfo", {})
        identifiers = vol.get("industryIdentifiers", [])
        isbn = ""
        for ident in identifiers:
            if ident.get("type") == "ISBN_13":
                isbn = ident.get("identifier", "")
                break
            elif ident.get("type") == "ISBN_10":
                isbn = ident.get("identifier", "")

        authors = vol.get("authors", [])
        book = {
            "title": vol.get("title", ""),
            "author": authors[0] if authors else "",
            "isbn": isbn,
            "publication_year": vol.get("publishedDate", "")[:4],
            "summary": vol.get("description", ""),
            "google_books_id": item.get("id", ""),
            "page_count": vol.get("pageCount", 0),
            "categories": vol.get("categories", []),
            "source": "google_books",
        }
        books.append(book)

    return books


def search_by_category(category_name: str, keywords: List[str],
                        limit_per_query: int = 20) -> List[Dict]:
    """Search Google Books across multiple keywords for a category."""
    all_books = []

    for kw in keywords:
        results = search_books(kw, max_results=limit_per_query)
        for b in results:
            b["category"] = category_name
        all_books.extend(results)

    return all_books


def get_book_preview_text(google_books_id: str) -> Optional[str]:
    """Try to get preview/snippet text for a book.

    Note: Google Books API does not directly provide full text.
    This gets the description/summary as a fallback.
    """
    if not google_books_id:
        return None
    try:
        rate_limit(0.5)
        url = f"{SEARCH_URL}/{google_books_id}"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        vol = data.get("volumeInfo", {})
        description = vol.get("description", "")
        return description if description else None
    except Exception as e:
        print(f"[GoogleBooks] Failed to get preview for {google_books_id}: {e}")
        return None
