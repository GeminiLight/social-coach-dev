"""
Knowledge extraction pipeline: Extract structured knowledge items from book summaries.

Supports two backends:
  - "api": Call an external LLM API (OpenAI-compatible)
  - "template": Rule-based template extraction (no LLM needed, for testing)

Usage:
    python -m src.extractor --backend template   # fast, no API needed
    python -m src.extractor --backend api --api-base http://localhost:11434/v1 --model qwen3-235b
"""

import csv
import json
import os
import re
import argparse
from typing import List, Dict, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_schemas() -> Dict:
    with open(os.path.join(PROJECT_ROOT, "config", "schemas.json"), "r") as f:
        return json.load(f)


def load_books(csv_path: str) -> List[Dict]:
    with open(csv_path, "r", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("summary")]


# ── LLM API Backend ──────────────────────────────────────────────────

def call_llm_api(prompt: str, api_base: str, model: str, api_key: str = "") -> str:
    """Call an OpenAI-compatible API."""
    import requests
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2048,
    }
    resp = requests.post(f"{api_base}/chat/completions", json=payload,
                         headers=headers, timeout=120)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def extract_with_api(book: Dict, schemas: Dict, api_base: str, model: str,
                     api_key: str = "") -> Dict:
    """Extract knowledge items from one book using LLM API."""
    title = book["title"]
    author = book.get("author", "")
    category = book.get("category", "")
    summary = book["summary"]

    prompt = f"""You are a social skills education expert. Given a book's metadata and summary, extract structured knowledge items.

Book: "{title}" by {author}
Category: {category}
Summary: {summary}

Extract the following as a JSON object:
1. "theories": list of 2-3 strategic theories (each with "principle", "explanation", "application")
2. "cases": list of 2-3 illustrative cases (each with "context", "action", "outcome", "lesson")
3. "scenarios": list of 1 practical scenario (with "title", "background", "characters" as list of {{"name","role"}}, "objective", "challenge")

Return ONLY valid JSON, no markdown fences."""

    try:
        raw = call_llm_api(prompt, api_base, model, api_key)
        # Try to parse JSON from response
        raw = raw.strip()
        if raw.startswith("```"):
            raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`")
        result = json.loads(raw)
        return result
    except Exception as e:
        print(f"  API extraction failed for '{title}': {e}")
        return {}


# ── Template Backend (no LLM) ────────────────────────────────────────

def extract_with_template(book: Dict, schemas: Dict) -> Dict:
    """Extract knowledge items using rule-based templates from book summary.

    This generates reasonable structured items by analyzing the summary text
    and the book's category/topic. Works without any LLM.
    """
    title = book["title"]
    author = book.get("author", "Unknown")
    category = book.get("category", "Social Skills")
    summary = book.get("summary", "")

    # Split summary into sentences for content sourcing
    sentences = [s.strip() for s in re.split(r'[.!?]+', summary) if len(s.strip()) > 20]

    # ── Theories ──
    theories = []
    # Theory 1: derived from book's core premise
    theories.append({
        "principle": f"According to '{title}' by {author}, effective {category.lower()} "
                     f"requires deliberate practice and self-awareness.",
        "explanation": sentences[0] + "." if sentences else
                       f"This book explores the foundations of {category.lower()} "
                       f"and provides evidence-based strategies for improvement.",
        "application": f"Apply the core framework from this work by reflecting on your "
                       f"{category.lower()} patterns and practicing alternative approaches "
                       f"in low-stakes situations first."
    })
    # Theory 2: derived from a key insight
    if len(sentences) > 1:
        theories.append({
            "principle": sentences[1] + "." if not sentences[1].endswith(".") else sentences[1],
            "explanation": f"This insight from '{title}' highlights how understanding "
                          f"the underlying dynamics of {category.lower()} can transform "
                          f"interpersonal interactions.",
            "application": f"When facing a {category.lower()} challenge, pause to consider "
                          f"this principle before reacting."
        })
    # Theory 3
    if len(sentences) > 2:
        theories.append({
            "principle": sentences[2] + "." if not sentences[2].endswith(".") else sentences[2],
            "explanation": f"Research cited in '{title}' demonstrates that this approach "
                          f"leads to measurably better outcomes in social interactions.",
            "application": f"Practice this by identifying one situation this week where "
                          f"you can consciously apply this principle."
        })

    # ── Cases ──
    cases = []
    case_contexts = [
        ("workplace meeting", "a colleague disagreed with their proposal"),
        ("family dinner", "a sensitive topic arose unexpectedly"),
        ("team project", "communication broke down between members"),
    ]
    for i, (ctx, trigger) in enumerate(case_contexts):
        if i >= 2 and len(sentences) < 3:
            break
        source_sent = sentences[min(i, len(sentences)-1)] if sentences else \
            f"The book discusses handling {category.lower()} challenges"
        cases.append({
            "context": f"During a {ctx}, {trigger}.",
            "action": f"Drawing on the principles of {category.lower()} from '{title}', "
                      f"the person paused, acknowledged the other's perspective, and "
                      f"reframed the conversation constructively.",
            "outcome": f"The situation de-escalated and both parties found common ground, "
                       f"strengthening their relationship.",
            "lesson": f"{source_sent}." if not source_sent.endswith(".") else source_sent
        })

    # ── Scenarios ──
    scenario_templates = {
        "Emotional Intelligence": {
            "title": f"Navigating an Emotional Workplace Crisis",
            "bg": "A team member just received bad personal news and is visibly upset during an important meeting.",
            "chars": [
                {"name": "You", "role": "Team lead who notices the distress"},
                {"name": "Alex", "role": "The upset team member"},
                {"name": "Jordan", "role": "Another colleague unaware of the situation"}
            ],
            "obj": "Support Alex while keeping the meeting productive",
            "challenge": "Balancing empathy for Alex's emotional state with professional responsibilities"
        },
        "Leadership": {
            "title": "Leading Through Disagreement",
            "bg": "Your team is split on a critical project direction. Two vocal members have opposing views and tensions are rising.",
            "chars": [
                {"name": "You", "role": "Team leader facilitating the decision"},
                {"name": "Sam", "role": "Advocates for the conservative approach"},
                {"name": "Riley", "role": "Pushes for the innovative but risky option"}
            ],
            "obj": "Guide the team to a decision everyone can support",
            "challenge": "Mediating between strong personalities while making a sound decision"
        },
        "Communication": {
            "title": "The Difficult Feedback Conversation",
            "bg": "You need to give constructive feedback to a sensitive colleague whose work quality has declined recently.",
            "chars": [
                {"name": "You", "role": "Manager delivering feedback"},
                {"name": "Pat", "role": "The colleague who is usually high-performing but struggling lately"}
            ],
            "obj": "Deliver honest feedback while maintaining the relationship and motivating improvement",
            "challenge": "Being direct without causing defensiveness or damaging trust"
        },
        "Negotiation": {
            "title": "The Salary Negotiation",
            "bg": "You have received a job offer with a salary below your expectations. You want the role but need better compensation.",
            "chars": [
                {"name": "You", "role": "Candidate negotiating the offer"},
                {"name": "Morgan", "role": "Hiring manager who presented the offer"}
            ],
            "obj": "Negotiate a fair compensation package while preserving the positive relationship",
            "challenge": "Advocating for your worth without seeming ungrateful or aggressive"
        },
        "Conflict Resolution": {
            "title": "The Roommate Dispute",
            "bg": "You and your roommate have escalating disagreements about household responsibilities and noise levels.",
            "chars": [
                {"name": "You", "role": "Roommate seeking resolution"},
                {"name": "Casey", "role": "Roommate with different living standards"}
            ],
            "obj": "Establish mutually agreeable living arrangements",
            "challenge": "Addressing built-up resentment while finding a fair compromise"
        },
        "Empathy": {
            "title": "Supporting a Grieving Friend",
            "bg": "Your close friend recently experienced a significant loss and is withdrawing from social activities.",
            "chars": [
                {"name": "You", "role": "Supportive friend"},
                {"name": "Taylor", "role": "Friend dealing with grief"}
            ],
            "obj": "Provide meaningful emotional support without being intrusive",
            "challenge": "Knowing when to listen, when to speak, and when to simply be present"
        },
        "Relationships": {
            "title": "Rebuilding Trust After a Misunderstanding",
            "bg": "A close friend believes you shared their private information, though it was actually someone else.",
            "chars": [
                {"name": "You", "role": "The wrongly accused friend"},
                {"name": "Jamie", "role": "The upset friend who feels betrayed"}
            ],
            "obj": "Clarify the misunderstanding and restore the friendship",
            "challenge": "Managing your own frustration at being wrongly accused while validating Jamie's feelings"
        },
        "Self-Awareness": {
            "title": "Recognizing Your Trigger in a Meeting",
            "bg": "During a team review, a colleague's critique of your work triggers a strong emotional reaction.",
            "chars": [
                {"name": "You", "role": "Team member receiving critical feedback"},
                {"name": "Devon", "role": "Colleague giving the critique"},
                {"name": "Manager", "role": "Observing the interaction"}
            ],
            "obj": "Manage your emotional response and engage constructively with the feedback",
            "challenge": "Separating your emotional reaction from the valid content of the critique"
        },
        "Social Intelligence": {
            "title": "Reading the Room at a Networking Event",
            "bg": "You're at a professional networking event where you need to make connections but are unsure how to approach groups already in conversation.",
            "chars": [
                {"name": "You", "role": "Professional seeking to expand network"},
                {"name": "Group A", "role": "Three people in an animated discussion"},
                {"name": "Loner", "role": "Someone standing alone by the refreshments"}
            ],
            "obj": "Successfully join conversations and make at least two meaningful connections",
            "challenge": "Reading social cues to know when and how to join existing conversations"
        },
        "Self-Management": {
            "title": "Staying Composed Under Pressure",
            "bg": "You're presenting a project proposal to senior leadership when an executive aggressively challenges your data and conclusions.",
            "chars": [
                {"name": "You", "role": "Presenter defending your proposal"},
                {"name": "Executive", "role": "Senior leader challenging your work"},
                {"name": "Your Manager", "role": "Silently observing your response"}
            ],
            "obj": "Address the challenge professionally while maintaining your credibility",
            "challenge": "Managing stress and defensiveness while thinking clearly under attack"
        },
    }

    # Pick template matching category, or default
    tmpl = scenario_templates.get(category, scenario_templates["Communication"])
    scenarios = [{
        "title": tmpl["title"],
        "background": tmpl["bg"],
        "characters": tmpl["chars"],
        "objective": tmpl["obj"],
        "challenge": tmpl["challenge"],
    }]

    return {
        "theories": theories,
        "cases": cases,
        "scenarios": scenarios,
    }


# ── Main Extraction Loop ─────────────────────────────────────────────

def run_extraction(books_csv: str, output_path: str, backend: str = "template",
                   api_base: str = "", model: str = "", api_key: str = ""):
    """Run extraction on all books."""
    schemas = load_schemas()
    books = load_books(books_csv)
    print(f"Loaded {len(books)} books with summaries")

    all_items = []
    stats = {"theories": 0, "cases": 0, "scenarios": 0, "failed": 0}

    for i, book in enumerate(books):
        if backend == "api":
            result = extract_with_api(book, schemas, api_base, model, api_key)
        else:
            result = extract_with_template(book, schemas)

        if not result:
            stats["failed"] += 1
            continue

        book_meta = {
            "book_title": book["title"],
            "book_author": book.get("author", ""),
            "book_category": book.get("category", ""),
            "book_id": book.get("book_id", ""),
        }

        for theory in result.get("theories", []):
            theory["type"] = "theory"
            theory.update(book_meta)
            all_items.append(theory)
            stats["theories"] += 1

        for case in result.get("cases", []):
            case["type"] = "case"
            case.update(book_meta)
            all_items.append(case)
            stats["cases"] += 1

        for scenario in result.get("scenarios", []):
            scenario["type"] = "scenario"
            scenario.update(book_meta)
            all_items.append(scenario)
            stats["scenarios"] += 1

        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{len(books)} books...")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"\nExtraction complete:")
    print(f"  Theories: {stats['theories']}")
    print(f"  Cases: {stats['cases']}")
    print(f"  Scenarios: {stats['scenarios']}")
    print(f"  Total items: {len(all_items)}")
    print(f"  Failed books: {stats['failed']}")
    print(f"  Saved to: {output_path}")

    return all_items


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["template", "api"], default="template")
    parser.add_argument("--api-base", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--input", default=os.path.join(PROJECT_ROOT, "data", "books_selected_200.csv"))
    parser.add_argument("--output", default=os.path.join(PROJECT_ROOT, "data", "corpus_extracted.json"))
    args = parser.parse_args()

    run_extraction(args.input, args.output, args.backend,
                   args.api_base, args.model, args.api_key)
