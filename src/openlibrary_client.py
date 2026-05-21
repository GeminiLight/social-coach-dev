"""OpenLibrary API client for searching and downloading social skills books."""

import requests
from typing import List, Dict, Optional
from src.utils import rate_limit, normalize_title


BASE_URL = "https://openlibrary.org"
SEARCH_URL = f"{BASE_URL}/search.json"


def search_books(query: str, subject: str = "", limit: int = 30) -> List[Dict]:
    """Search OpenLibrary for books by query and optional subject.

    Returns list of book metadata dicts.
    """
    params = {
        "q": query,
        "limit": limit,
        "language": "eng",
        "fields": "key,title,author_name,first_publish_year,isbn,subject,edition_count,has_fulltext,ia",
    }
    if subject:
        params["subject"] = subject

    try:
        rate_limit(1.0)
        resp = requests.get(SEARCH_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[OpenLibrary] Search failed for '{query}': {e}")
        return []

    books = []
    for doc in data.get("docs", []):
        authors = doc.get("author_name", [])
        isbns = doc.get("isbn", [])
        book = {
            "title": doc.get("title", ""),
            "author": authors[0] if authors else "",
            "isbn": isbns[0] if isbns else "",
            "publication_year": str(doc.get("first_publish_year", "")),
            "openlibrary_key": doc.get("key", ""),
            "has_fulltext": doc.get("has_fulltext", False),
            "ia_ids": doc.get("ia", []),
            "edition_count": doc.get("edition_count", 0),
            "source": "openlibrary",
        }
        books.append(book)

    return books


def search_by_category(category_name: str, keywords: List[str], subjects: List[str],
                        limit_per_query: int = 20) -> List[Dict]:
    """Search OpenLibrary across multiple keywords/subjects for a category."""
    all_books = []

    for kw in keywords:
        results = search_books(kw, limit=limit_per_query)
        for b in results:
            b["category"] = category_name
        all_books.extend(results)

    for subj in subjects:
        results = search_books(subj, subject=subj, limit=limit_per_query)
        for b in results:
            b["category"] = category_name
        all_books.extend(results)

    return all_books


def get_book_text_url(openlibrary_key: str) -> Optional[str]:
    """Check if full text is available for a book and return the text URL."""
    if not openlibrary_key:
        return None
    try:
        rate_limit(0.5)
        url = f"{BASE_URL}{openlibrary_key}.json"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # Check for Internet Archive availability via OCAID
        ocaid = None
        if "ocaid" in data:
            ocaid = data["ocaid"]
        elif "ia_loaded_id" in data:
            ia_ids = data["ia_loaded_id"]
            if ia_ids:
                ocaid = ia_ids[0]

        if ocaid:
            return f"https://archive.org/download/{ocaid}/{ocaid}_djvu.txt"
        return None
    except Exception as e:
        print(f"[OpenLibrary] Failed to get text URL for {openlibrary_key}: {e}")
        return None


def download_book_text(ia_ids: List[str]) -> Optional[str]:
    """Try to download full text from Internet Archive for given IA identifiers."""
    for ia_id in ia_ids[:3]:  # Try up to 3 IA identifiers
        txt_url = f"https://archive.org/download/{ia_id}/{ia_id}_djvu.txt"
        try:
            rate_limit(1.0)
            resp = requests.get(txt_url, timeout=60)
            if resp.status_code == 200 and len(resp.text) > 1000:
                return resp.text
        except Exception:
            continue

        # Try alternative text format
        alt_url = f"https://archive.org/stream/{ia_id}/{ia_id}_djvu.txt"
        try:
            rate_limit(0.5)
            resp = requests.get(alt_url, timeout=60)
            if resp.status_code == 200 and len(resp.text) > 1000:
                return resp.text
        except Exception:
            continue

    return None
