"""
Download book full texts from Internet Archive for the selected 200 books.

Usage:
    python download_books.py                    # Download all
    python download_books.py --limit 10         # Download first 10 only (for testing)
    python download_books.py --stats            # Just print current download stats
"""

import argparse
import csv
import os
import sys

from tqdm import tqdm

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.archive_client import search_and_download
from src.utils import save_book_text

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
BOOKS_CSV = os.path.join(DATA_DIR, "books_selected_200.csv")
BOOKS_CONTENT_DIR = os.path.join(DATA_DIR, "books_content")


def download_all(limit: int = 0):
    """Download book texts from Internet Archive."""
    with open(BOOKS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        books = list(reader)

    os.makedirs(BOOKS_CONTENT_DIR, exist_ok=True)

    downloaded = 0
    already_done = 0
    not_found = 0
    total = min(len(books), limit) if limit > 0 else len(books)

    for i, book in enumerate(tqdm(books[:total], desc="Downloading")):
        book_id = book.get("book_id", "")
        title = book.get("title", "")
        author = book.get("author", "")

        # Skip if already downloaded
        if book.get("text_available") == "True":
            already_done += 1
            continue

        text, archive_id = search_and_download(title, author)

        if text:
            save_book_text(text, book_id, title, BOOKS_CONTENT_DIR)
            book["text_available"] = "True"
            book["text_source"] = "internet_archive"
            downloaded += 1
            if (downloaded % 5) == 0:
                tqdm.write(f"  [{downloaded}] Downloaded: {title[:60]}")
        else:
            book["text_available"] = "False"
            not_found += 1

    # Save updated CSV
    with open(BOOKS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(books)

    print(f"\nResults:")
    print(f"  Already downloaded: {already_done}")
    print(f"  Newly downloaded: {downloaded}")
    print(f"  Not found: {not_found}")
    print(f"  Total with text: {already_done + downloaded}/{total}")


def print_stats():
    """Print download statistics."""
    with open(BOOKS_CSV, "r", encoding="utf-8") as f:
        books = list(csv.DictReader(f))

    with_text = sum(1 for b in books if b.get("text_available") == "True")
    print(f"Total books: {len(books)}")
    print(f"With full text: {with_text}")
    print(f"Without text: {len(books) - with_text}")

    if os.path.exists(BOOKS_CONTENT_DIR):
        files = [f for f in os.listdir(BOOKS_CONTENT_DIR) if f.endswith(".txt")]
        total_size = sum(os.path.getsize(os.path.join(BOOKS_CONTENT_DIR, f)) for f in files)
        print(f"\nText files on disk: {len(files)}")
        print(f"Total size: {total_size / 1024 / 1024:.1f} MB")

        if files:
            sizes = [os.path.getsize(os.path.join(BOOKS_CONTENT_DIR, f)) for f in files]
            print(f"Avg file size: {sum(sizes)/len(sizes)/1024:.0f} KB")
            print(f"Largest: {max(sizes)/1024:.0f} KB")
            print(f"Smallest: {min(sizes)/1024:.0f} KB")


def main():
    parser = argparse.ArgumentParser(description="Download book texts from Internet Archive")
    parser.add_argument("--limit", type=int, default=0, help="Max books to process (0=all)")
    parser.add_argument("--stats", action="store_true", help="Print stats only")
    args = parser.parse_args()

    if args.stats:
        print_stats()
    else:
        download_all(args.limit)
        print()
        print_stats()


if __name__ == "__main__":
    main()
