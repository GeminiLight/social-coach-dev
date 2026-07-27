#!/usr/bin/env python3
"""Export the selected SocialCoach books as a readable Markdown catalog.

The script uses only the Python standard library and does not fetch or modify
book metadata. It validates the selected CSV before writing the catalog.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "books_selected_200.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "books_selected_200.md"
DEFAULT_REQUIRED_TITLES = (
    "Nonviolent Communication: A Language of Life",
    "Emotional Intelligence: Why It Can Matter More Than IQ",
)
REQUIRED_COLUMNS = {
    "book_id",
    "title",
    "author",
    "isbn",
    "publication_year",
    "category",
    "source",
}


def normalize_text(value: str) -> str:
    """Normalize text for duplicate and exact-title checks."""
    return re.sub(r"\s+", " ", value).strip().casefold()


def markdown_cell(value: str) -> str:
    """Escape text for use inside a Markdown table cell."""
    return re.sub(r"\s+", " ", value).strip().replace("|", r"\|")


def display_source(source: str) -> str:
    labels = {
        "curated_seed": "Curated seed",
        "google_books": "Google Books",
        "openlibrary": "Open Library",
        "internet_archive": "Internet Archive",
    }
    return labels.get(source, source.replace("_", " ").title())


def load_books(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            raise ValueError(f"missing required CSV columns: {', '.join(missing)}")
        return list(reader)


def validate_books(
    books: Iterable[dict[str, str]],
    expected_count: int,
    required_titles: Iterable[str],
) -> tuple[list[str], list[str]]:
    books = list(books)
    errors: list[str] = []
    warnings: list[str] = []

    if expected_count and len(books) != expected_count:
        errors.append(f"expected {expected_count} books, found {len(books)}")

    seen_ids: set[str] = set()
    seen_editions: set[tuple[str, str]] = set()
    for row_number, book in enumerate(books, start=2):
        title = book["title"].strip()
        author = book["author"].strip()
        book_id = book["book_id"].strip()
        if not title or not book_id:
            errors.append(
                f"row {row_number} must include book_id and title"
            )
            continue
        if not author:
            warnings.append(f"row {row_number} has no author: {title}")
        if not book["publication_year"].strip():
            warnings.append(f"row {row_number} has no publication year: {title}")

        if book_id in seen_ids:
            errors.append(f"duplicate book_id at row {row_number}: {book_id}")
        seen_ids.add(book_id)

        edition_key = (normalize_text(title), normalize_text(author))
        if edition_key in seen_editions:
            errors.append(
                f"duplicate title-author pair at row {row_number}: "
                f"{title} — {author}"
            )
        seen_editions.add(edition_key)

    available_titles = {normalize_text(book["title"]) for book in books}
    for title in required_titles:
        if normalize_text(title) not in available_titles:
            errors.append(f"required title not found: {title}")

    return errors, warnings


def render_markdown(books: list[dict[str, str]], source_path: Path) -> str:
    by_category: dict[str, list[dict[str, str]]] = defaultdict(list)
    for book in books:
        by_category[book["category"].strip() or "Uncategorized"].append(book)

    source_counts = Counter(book["source"].strip() or "unknown" for book in books)
    lines = [
        "# SocialCoach Book List",
        "",
        f"Generated from `{source_path.name}`. Total: **{len(books)} books** "
        f"across **{len(by_category)} categories**.",
        "",
        "This catalog reports bibliographic metadata only. Inclusion does not "
        "imply that the underlying full text may be redistributed.",
        "",
        "## Summary",
        "",
        "| Source | Books |",
        "|---|---:|",
    ]
    for source, count in sorted(source_counts.items()):
        lines.append(f"| {markdown_cell(display_source(source))} | {count} |")

    for category in sorted(by_category):
        category_books = sorted(
            by_category[category],
            key=lambda book: (
                normalize_text(book["title"]),
                normalize_text(book["author"]),
            ),
        )
        lines.extend(
            [
                "",
                f"## {category} ({len(category_books)})",
                "",
                "| # | Title | Author | Year | ISBN | Source |",
                "|---:|---|---|---:|---|---|",
            ]
        )
        for index, book in enumerate(category_books, start=1):
            lines.append(
                "| {index} | {title} | {author} | {year} | {isbn} | {source} |".format(
                    index=index,
                    title=markdown_cell(book["title"]),
                    author=markdown_cell(book["author"]) or "—",
                    year=markdown_cell(book["publication_year"]) or "—",
                    isbn=markdown_cell(book["isbn"]) or "—",
                    source=markdown_cell(display_source(book["source"])),
                )
            )

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and export the selected books as Markdown."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--expected-count",
        type=int,
        default=200,
        help="Fail unless the CSV contains this many books; use 0 to disable.",
    )
    parser.add_argument(
        "--required-title",
        action="append",
        dest="required_titles",
        help=(
            "Require an exact title after case/whitespace normalization. "
            "May be repeated."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()
    required_titles = args.required_titles or list(DEFAULT_REQUIRED_TITLES)

    try:
        books = load_books(input_path)
        errors, warnings = validate_books(
            books, args.expected_count, required_titles
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(books, input_path), encoding="utf-8")

    print(f"Validated {len(books)} books.")
    for title in required_titles:
        print(f"Found required title: {title}")
    print(f"Wrote Markdown catalog: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
