"""
Main orchestration script for book acquisition pipeline.

Usage:
    python main_acquire.py --step list       # Step 1: Build book list (seed + Google Books)
    python main_acquire.py --step enrich     # Step 2: Enrich metadata via Google Books
    python main_acquire.py --step select     # Step 3: Select top 200 books
    python main_acquire.py --step stats      # Step 4: Print statistics
    python main_acquire.py --step all        # Run all steps

Note: OpenLibrary and Gutenberg are disabled due to SSL issues in the current
environment. The pipeline uses curated seed list (~125 books) + Google Books
API expansion to reach ~200 books.
"""

import argparse
import os
import sys

from tqdm import tqdm

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.book_scraper import get_seed_books
from src.google_books_client import (
    search_by_category as gb_search,
    search_books as gb_search_single,
)
from src.utils import (
    deduplicate_books,
    save_books_csv,
    load_books_csv,
    load_categories,
    normalize_title,
)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
BOOKS_CSV = os.path.join(DATA_DIR, "books_metadata.csv")
BOOKS_SELECTED_CSV = os.path.join(DATA_DIR, "books_selected_200.csv")
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "categories.json")


def step_build_book_list():
    """Step 1: Aggregate book lists from seed + Google Books and deduplicate."""
    print("=" * 60)
    print("Step 1: Building book list from all sources")
    print("=" * 60)

    all_books = []

    # Source 1: Curated seed list (~125 books)
    print("\n[1/2] Loading curated seed list...")
    seed_books = get_seed_books()
    print(f"  Got {len(seed_books)} seed books")
    all_books.extend(seed_books)

    # Source 2: Google Books search to expand coverage
    print("\n[2/2] Searching Google Books for additional books...")
    categories = load_categories(CONFIG_PATH)

    # Collect seed titles to avoid fetching them again
    seed_titles = {normalize_title(b["title"]) for b in seed_books}

    for cat in tqdm(categories, desc="  Google Books"):
        try:
            results = gb_search(cat["name"], cat["keywords"], limit_per_query=15)
            # Filter out books we already have
            new_results = [
                b for b in results
                if normalize_title(b.get("title", "")) not in seed_titles
            ]
            all_books.extend(new_results)
        except Exception as e:
            print(f"  Warning: Google Books search failed for {cat['name']}: {e}")

    # Deduplicate
    print(f"\nTotal raw books: {len(all_books)}")
    unique_books = deduplicate_books(all_books)
    print(f"After deduplication: {len(unique_books)}")

    # Sort by category
    unique_books.sort(key=lambda b: (b.get("category", ""), b.get("title", "")))

    # Save
    save_books_csv(unique_books, BOOKS_CSV)
    print(f"\nBook list saved to {BOOKS_CSV}")

    return unique_books


def step_enrich_metadata():
    """Step 2: Enrich book metadata with Google Books summaries."""
    print("=" * 60)
    print("Step 2: Enriching metadata via Google Books")
    print("=" * 60)

    books = load_books_csv(BOOKS_CSV)
    if not books:
        print("No books found. Run --step list first.")
        return []

    enriched = 0
    for book in tqdm(books, desc="  Enriching"):
        if book.get("summary"):
            continue

        title = book.get("title", "")
        author = book.get("author", "")
        if not title:
            continue

        try:
            query = f'intitle:"{title}" inauthor:"{author}"' if author else f'intitle:"{title}"'
            results = gb_search_single(query, max_results=1)
            if results:
                r = results[0]
                if not book.get("summary"):
                    book["summary"] = r.get("summary", "")
                if not book.get("isbn") and r.get("isbn"):
                    book["isbn"] = r["isbn"]
                if not book.get("google_books_id") and r.get("google_books_id"):
                    book["google_books_id"] = r["google_books_id"]
                enriched += 1
        except Exception:
            continue

    print(f"\nEnriched {enriched} books with additional metadata")
    save_books_csv(books, BOOKS_CSV)
    return books


def step_select_top_200():
    """Step 3: Select top 200 books with balanced category distribution.

    Priority: curated_seed > google_books with summary > google_books without.
    Aim for ~20 books per category.
    """
    print("=" * 60)
    print("Step 3: Selecting top 200 books")
    print("=" * 60)

    books = load_books_csv(BOOKS_CSV)
    if not books:
        print("No books found. Run --step list first.")
        return []

    # Score each book for selection priority
    def score_book(b):
        s = 0
        if b.get("source") == "curated_seed":
            s += 100  # curated gets highest priority
        if b.get("summary"):
            s += 10   # having a summary is valuable
        if b.get("isbn"):
            s += 5    # having ISBN helps traceability
        return s

    # Group by category
    by_category = {}
    for b in books:
        cat = b.get("category", "Unknown")
        by_category.setdefault(cat, []).append(b)

    # Sort within each category by score
    for cat in by_category:
        by_category[cat].sort(key=score_book, reverse=True)

    # Select ~20 per category, filling up to 200
    target = 200
    per_cat = target // len(by_category)  # ~20
    selected = []

    # First pass: take top per_cat from each category
    remaining = {}
    for cat, cat_books in by_category.items():
        selected.extend(cat_books[:per_cat])
        remaining[cat] = cat_books[per_cat:]

    # Second pass: fill remaining slots from leftover books
    leftover = []
    for cat in remaining:
        leftover.extend(remaining[cat])
    leftover.sort(key=score_book, reverse=True)

    slots_left = target - len(selected)
    if slots_left > 0:
        selected.extend(leftover[:slots_left])

    # Ensure exactly 200 (or as close as possible)
    selected = selected[:target]

    # Re-sort
    selected.sort(key=lambda b: (b.get("category", ""), b.get("title", "")))

    save_books_csv(selected, BOOKS_SELECTED_CSV)
    print(f"\nSelected {len(selected)} books -> {BOOKS_SELECTED_CSV}")

    # Quick distribution
    cats = {}
    for b in selected:
        cat = b.get("category", "Unknown")
        cats[cat] = cats.get(cat, 0) + 1
    print("\nCategory distribution:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        src_counts = {}
        for b in selected:
            if b.get("category") == cat:
                src = b.get("source", "unknown")
                src_counts[src] = src_counts.get(src, 0) + 1
        detail = ", ".join(f"{s}:{c}" for s, c in src_counts.items())
        print(f"  {cat}: {count} ({detail})")

    return selected


def step_print_stats():
    """Step 3: Print statistics about the acquired books."""
    print("=" * 60)
    print("Book Acquisition Statistics")
    print("=" * 60)

    books = load_books_csv(BOOKS_CSV)
    if not books:
        print("No books found. Run --step list first.")
        return

    print(f"\nTotal books: {len(books)}")

    # By category
    categories = {}
    for b in books:
        cat = b.get("category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1
    print("\nBooks per category:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    # By source
    sources = {}
    for b in books:
        src = b.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1
    print("\nBooks per source:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {src}: {count}")

    # Summary availability
    with_summary = sum(1 for b in books if b.get("summary"))
    with_isbn = sum(1 for b in books if b.get("isbn"))
    print(f"\nMetadata completeness:")
    print(f"  With summary: {with_summary}/{len(books)}")
    print(f"  With ISBN: {with_isbn}/{len(books)}")


def main():
    parser = argparse.ArgumentParser(description="Book Acquisition Pipeline")
    parser.add_argument(
        "--step",
        choices=["list", "enrich", "select", "stats", "all"],
        default="all",
        help="Which step to run",
    )
    args = parser.parse_args()

    if args.step in ("list", "all"):
        step_build_book_list()

    if args.step in ("enrich", "all"):
        step_enrich_metadata()

    if args.step in ("select", "all"):
        step_select_top_200()

    if args.step in ("stats", "all"):
        step_print_stats()


if __name__ == "__main__":
    main()
