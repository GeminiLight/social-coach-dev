"""Validate extracted knowledge items against schema requirements."""

import json
import os
from typing import List, Dict, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FIELDS = {
    "theory": ["principle", "explanation", "application"],
    "case": ["context", "action", "outcome", "lesson"],
    "scenario": ["title", "background", "characters", "objective", "challenge"],
}


def validate_item(item: Dict) -> Tuple[bool, str]:
    """Validate a single knowledge item. Returns (is_valid, reason)."""
    item_type = item.get("type", "")
    if item_type not in REQUIRED_FIELDS:
        return False, f"Unknown type: {item_type}"

    for field in REQUIRED_FIELDS[item_type]:
        val = item.get(field)
        if not val:
            return False, f"Missing or empty field: {field}"
        if isinstance(val, str) and len(val.strip()) < 10:
            return False, f"Field too short: {field} (len={len(val.strip())})"

    # Scenario-specific: characters must be a list
    if item_type == "scenario":
        chars = item.get("characters", [])
        if not isinstance(chars, list) or len(chars) < 2:
            return False, "Scenario must have at least 2 characters"

    return True, "OK"


def run_validation(input_path: str, output_path: str) -> List[Dict]:
    """Validate all items and save only valid ones."""
    with open(input_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    valid = []
    invalid_count = 0
    reasons = {}

    for item in items:
        is_valid, reason = validate_item(item)
        if is_valid:
            valid.append(item)
        else:
            invalid_count += 1
            reasons[reason] = reasons.get(reason, 0) + 1

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(valid, f, ensure_ascii=False, indent=2)

    print(f"Validation: {len(valid)} valid, {invalid_count} invalid out of {len(items)}")
    if reasons:
        print("  Rejection reasons:")
        for r, c in sorted(reasons.items(), key=lambda x: -x[1]):
            print(f"    {r}: {c}")
    print(f"  Saved to: {output_path}")
    return valid


if __name__ == "__main__":
    input_p = os.path.join(PROJECT_ROOT, "data", "corpus_extracted.json")
    output_p = os.path.join(PROJECT_ROOT, "data", "corpus_validated.json")
    run_validation(input_p, output_p)
