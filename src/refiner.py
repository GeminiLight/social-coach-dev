"""Refine knowledge items: clean text, fix inconsistencies, assign final IDs."""

import json
import os
import re
import hashlib
from typing import List, Dict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s([.,;:!?])', r'\1', text)
    # Ensure ends with period
    if text and text[-1] not in '.!?':
        text += '.'
    return text


def generate_item_id(item: Dict, idx: int) -> str:
    """Generate a unique ID for a knowledge item."""
    content = json.dumps(item, sort_keys=True)
    h = hashlib.md5(content.encode()).hexdigest()[:8]
    prefix = {"theory": "TH", "case": "CA", "scenario": "SC"}.get(item.get("type", ""), "XX")
    return f"{prefix}_{idx:05d}_{h}"


def refine_item(item: Dict) -> Dict:
    """Clean and refine a single item."""
    # Clean all string fields
    for key in list(item.keys()):
        if isinstance(item[key], str) and key not in ("type", "item_id", "book_id"):
            item[key] = clean_text(item[key])

    # For scenarios, ensure characters is properly formatted
    if item.get("type") == "scenario":
        chars = item.get("characters", [])
        if isinstance(chars, list):
            cleaned_chars = []
            for c in chars:
                if isinstance(c, dict):
                    cleaned_chars.append({
                        "name": c.get("name", "Unknown"),
                        "role": c.get("role", "Participant"),
                    })
                elif isinstance(c, str):
                    cleaned_chars.append({"name": c, "role": "Participant"})
            item["characters"] = cleaned_chars

    return item


def run_refinement(input_path: str, output_path: str) -> List[Dict]:
    """Refine all items and produce final corpus."""
    with open(input_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    refined = []
    for idx, item in enumerate(items):
        item = refine_item(item)
        item["item_id"] = generate_item_id(item, idx)
        refined.append(item)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(refined, f, ensure_ascii=False, indent=2)

    # Stats
    type_counts = {}
    for item in refined:
        t = item.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f"Refinement complete: {len(refined)} items")
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}")
    print(f"Saved to: {output_path}")

    return refined


if __name__ == "__main__":
    input_p = os.path.join(PROJECT_ROOT, "data", "corpus_tagged.json")
    output_p = os.path.join(PROJECT_ROOT, "data", "corpus_final.json")
    run_refinement(input_p, output_p)
