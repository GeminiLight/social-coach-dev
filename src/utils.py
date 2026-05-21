"""Common utilities for book acquisition pipeline."""

import time
import hashlib
import re
import csv
import json
import os
from typing import List, Dict, Optional


def rate_limit(seconds: float = 1.0):
    """Simple rate limiter - sleep between requests."""
    time.sleep(seconds)


def normalize_title(title: str) -> str:
    """Normalize book title for deduplication."""
    title = title.lower().strip()
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title


def generate_book_id(title: str, author: str) -> str:
    """Generate a unique ID for a book based on title + author."""
    key = f"{normalize_title(title)}_{author.lower().strip()}"
    return hashlib.md5(key.encode()).hexdigest()[:12]


def deduplicate_books(books: List[Dict]) -> List[Dict]:
    """Remove duplicate books based on normalized title + author."""
    seen = set()
    unique = []
    for book in books:
        book_id = generate_book_id(book.get('title', ''), book.get('author', ''))
        if book_id not in seen:
            seen.add(book_id)
            book['book_id'] = book_id
            unique.append(book)
    return unique


def save_books_csv(books: List[Dict], filepath: str):
    """Save books metadata to CSV."""
    if not books:
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = [
        'book_id', 'title', 'author', 'isbn', 'publication_year',
        'category', 'source', 'summary', 'openlibrary_key',
        'gutenberg_id', 'google_books_id', 'text_available', 'text_source'
    ]
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(books)
    print(f"Saved {len(books)} books to {filepath}")


def load_books_csv(filepath: str) -> List[Dict]:
    """Load books metadata from CSV."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_categories(config_path: str) -> List[Dict]:
    """Load category definitions from config."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config['categories']


def sanitize_filename(name: str) -> str:
    """Create a safe filename from a string."""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '_', name.strip())
    return name[:100]


def save_book_text(text: str, book_id: str, title: str, output_dir: str):
    """Save book text to a file."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{book_id}_{sanitize_filename(title)}.txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    return filepath
