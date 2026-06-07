# Social Coach

LLM-powered social coaching system that extracts actionable social skills from books and applies them to real-world scenarios.

## Overview

The pipeline scrapes books from multiple public sources, extracts social coaching concepts using LLMs, tags and validates them, then refines the final corpus for downstream use.

## Pipeline

```
Book Sources → Scraper → Extractor → Tagger → Validator → Refiner → Final Corpus
```

1. **Scraping**: Collects book content from Gutenberg, Open Library, Internet Archive, Google Books
2. **Extraction**: Uses LLMs to extract social coaching concepts from book text
3. **Tagging**: Categorizes extracted concepts
4. **Validation**: Filters and validates quality
5. **Refinement**: Produces the final curated corpus

## Structure

```
src/
  book_scraper.py           # Multi-source book scraper
  archive_client.py         # Internet Archive client
  google_books_client.py    # Google Books client
  gutenberg_client.py       # Project Gutenberg client
  openlibrary_client.py     # Open Library client
  extractor.py              # LLM-based concept extraction
  tagger.py                 # Concept tagging
  validator.py              # Quality validation
  refiner.py                # Corpus refinement
  utils.py                  # Shared utilities
data/
  books_metadata.csv        # Metadata for selected books
  books_selected_200.csv    # 200 selected books
  books_content/            # Local-only downloaded book texts
  corpus_extracted.json     # Raw extracted concepts
  corpus_tagged.json        # Tagged concepts
  corpus_validated.json     # Validated concepts
  corpus_final.json         # Final curated corpus
```

The manuscript is maintained separately in the `social-coach-paper` repository. Raw downloaded book texts and run logs are intentionally kept local and are not committed to the public development repository.

## Project Page

The polished paper homepage is in `docs/` and can be served directly by GitHub Pages. It includes the static HTML/CSS/JS site, paper PDF, visual assets, citation metadata, structured data, `sitemap.xml`, `robots.txt`, and `llms.txt` for SEO/GEO.

Local preview:

```bash
python3 -m http.server 4173 --directory docs
```

## Usage

```bash
python src/book_scraper.py      # Scrape books
python src/extractor.py         # Extract concepts
python src/tagger.py            # Tag concepts
python src/validator.py         # Validate
python src/refiner.py           # Refine final corpus
```
