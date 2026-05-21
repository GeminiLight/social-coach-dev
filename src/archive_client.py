"""Internet Archive client for searching and downloading book full texts.

archive.org is accessible from this environment (unlike openlibrary.org/gutenberg.org).
Uses the Archive.org Advanced Search API and direct file downloads.
"""

import requests
import re
import urllib.parse
from typing import List, Dict, Optional, Tuple
from src.utils import rate_limit


SEARCH_URL = "https://archive.org/advancedsearch.php"
META_URL = "https://archive.org/metadata"
DOWNLOAD_URL = "https://archive.org/download"


def search_book(title: str, author: str = "") -> Optional[Dict]:
    """Search Internet Archive for a specific book by title and author.

    Tries multiple query strategies: title+author, then title-only fallback.
    Returns the best matching item's metadata, or None.
    """
    queries = []

    # Clean title
    clean_title = re.sub(r'[:\-–—].*$', '', title).strip()  # Remove subtitle
    clean_title = re.sub(r'[^\w\s]', '', clean_title).strip()

    # Strategy 1: title + author
    if author:
        author_clean = author.split(",")[0].strip()
        queries.append(f"title:({clean_title}) AND creator:({author_clean}) AND mediatype:(texts)")

    # Strategy 2: title only
    queries.append(f"title:({clean_title}) AND mediatype:(texts)")

    for query in queries:
        params = {
            "q": query,
            "fl[]": ["identifier", "title", "creator", "year", "format"],
            "rows": 3,
            "output": "json",
        }
        try:
            rate_limit(0.5)
            resp = requests.get(SEARCH_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            docs = data.get("response", {}).get("docs", [])
            if docs:
                return docs[0]
        except Exception:
            continue

    return None


def get_text_file_url(identifier: str) -> Optional[str]:
    """Get the URL of the text file for a given Internet Archive identifier.

    Looks for _djvu.txt or .txt files in the item's file list.
    """
    try:
        rate_limit(0.3)
        url = f"{META_URL}/{identifier}/files"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        files = resp.json().get("result", [])

        # Priority: _djvu.txt > .txt (not metadata files)
        djvu_txt = None
        plain_txt = None

        for f in files:
            name = f.get("name", "")
            if name.endswith("_djvu.txt"):
                djvu_txt = name
            elif name.endswith(".txt") and not name.startswith("__") \
                    and "meta" not in name.lower() and f.get("size", "0") != "0":
                size = int(f.get("size", 0))
                if size > 5000:  # At least 5KB to be a real text
                    plain_txt = name

        chosen = djvu_txt or plain_txt
        if chosen:
            encoded_name = urllib.parse.quote(chosen)
            return f"{DOWNLOAD_URL}/{identifier}/{encoded_name}"
        return None
    except Exception:
        return None


def download_text(url: str) -> Optional[str]:
    """Download text content from a URL."""
    try:
        rate_limit(0.5)
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200 and len(resp.text) > 1000:
            return resp.text
        return None
    except Exception:
        return None


def search_and_download(title: str, author: str = "") -> Tuple[Optional[str], str]:
    """Search for a book and download its full text.

    Returns (text_content, archive_identifier) or (None, "").
    """
    doc = search_book(title, author)
    if not doc:
        return None, ""

    identifier = doc.get("identifier", "")
    if not identifier:
        return None, ""

    txt_url = get_text_file_url(identifier)
    if not txt_url:
        return None, identifier

    text = download_text(txt_url)
    return text, identifier
