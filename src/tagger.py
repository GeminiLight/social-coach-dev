"""Tag knowledge items with CASEL competency, social skill, and scenario context."""

import json
import os
import re
from typing import List, Dict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_taxonomies() -> Dict:
    with open(os.path.join(PROJECT_ROOT, "config", "schemas.json"), "r") as f:
        return json.load(f)["tag_taxonomies"]


# ── Keyword-based tag inference ──

COMPETENCY_KEYWORDS = {
    "Self-Awareness": [
        "self-aware", "recognize", "identify emotion", "bias", "reflect",
        "introspect", "understand yourself", "self-knowledge", "mindset",
        "trigger", "personal growth", "insight", "self-perception",
    ],
    "Self-Management": [
        "self-control", "impulse", "regulate", "stress", "discipline",
        "persever", "goal", "habit", "motivation", "resilience", "manage",
        "willpower", "composure", "patience", "focus", "burnout",
    ],
    "Social Awareness": [
        "empathy", "perspective", "compassion", "diversity", "social norm",
        "cultural", "belonging", "understand others", "appreciate",
        "grateful", "kindness", "inclusive",
    ],
    "Relationship Skills": [
        "communicat", "relationship", "teamwork", "cooperat", "conflict",
        "resolve", "listen", "feedback", "trust", "collaborate", "bond",
        "negotiat", "leadership", "help", "support",
    ],
    "Responsible Decision-Making": [
        "decision", "consequence", "ethical", "responsible", "problem-solv",
        "analyze", "curious", "open-minded", "well-being", "reflect on role",
    ],
}

SKILL_KEYWORDS = {
    "Communication": ["communicat", "speak", "talk", "express", "articulate", "dialogue", "conversation"],
    "Empathy and compassion": ["empathy", "compassion", "understand feel", "care about"],
    "Perspective-taking": ["perspective", "point of view", "see from", "walk in shoes"],
    "Emotion regulation": ["emotion regulat", "manage emotion", "control feeling", "emotional agility"],
    "Building relationships": ["build relationship", "connect", "bond", "rapport", "friendship"],
    "Resolving conflicts": ["conflict", "resolve", "mediat", "de-escalat", "disagree"],
    "Leadership": ["leader", "lead", "inspire", "vision", "guide team"],
    "Goal-setting": ["goal", "objective", "target", "plan", "ambition"],
    "Stress management": ["stress", "burnout", "relax", "cope", "overwhelm"],
    "Self-discipline and motivation": ["discipline", "motivat", "habit", "willpower", "persist"],
    "Teamwork and working cooperatively": ["team", "cooperat", "collaborat", "group", "together"],
    "Self-efficacy": ["self-efficacy", "confidence", "believe in", "capable", "can do"],
    "Identifying emotions": ["identify emotion", "recognize feeling", "name emotion", "aware of emotion"],
    "Impulse control": ["impulse", "react", "pause before", "think before"],
    "Growth mindset": ["growth mindset", "learn from", "improve", "develop"],
    "Negotiation": ["negotiat", "bargain", "deal", "compromise", "persuad", "influence"],
}

CONTEXT_KEYWORDS = {
    "Workplace": ["work", "office", "meeting", "colleague", "boss", "manager", "professional", "career", "job", "interview"],
    "Family": ["family", "parent", "child", "sibling", "home", "spouse", "partner"],
    "Friendship": ["friend", "buddy", "pal", "social circle"],
    "Romantic": ["romantic", "dating", "partner", "love", "relationship"],
    "Education": ["school", "class", "student", "teacher", "learn", "university"],
    "Public/Stranger": ["stranger", "public", "store", "transport", "crowd"],
    "Party/Social": ["party", "event", "gathering", "network", "social"],
}


def infer_competency(text: str) -> str:
    """Infer CASEL competency from text content."""
    text_lower = text.lower()
    scores = {}
    for comp, keywords in COMPETENCY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[comp] = score
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Relationship Skills"


def infer_skill(text: str) -> str:
    """Infer specific social skill from text content."""
    text_lower = text.lower()
    scores = {}
    for skill, keywords in SKILL_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[skill] = score
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Communication"


def infer_context(text: str) -> str:
    """Infer scenario context from text content."""
    text_lower = text.lower()
    scores = {}
    for ctx, keywords in CONTEXT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[ctx] = score
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Workplace"


def get_item_text(item: Dict) -> str:
    """Concatenate all text fields for analysis."""
    parts = []
    for k, v in item.items():
        if isinstance(v, str) and k not in ("type", "book_id", "book_title", "book_author"):
            parts.append(v)
        elif isinstance(v, list):
            for entry in v:
                if isinstance(entry, dict):
                    parts.extend(str(x) for x in entry.values())
                else:
                    parts.append(str(entry))
    return " ".join(parts)


def tag_item(item: Dict) -> Dict:
    """Add competency, skill, and context tags to an item."""
    text = get_item_text(item)
    # Also use book category as a hint
    book_cat = item.get("book_category", "")
    combined = text + " " + book_cat

    item["competency_tag"] = infer_competency(combined)
    item["skill_tag"] = infer_skill(combined)
    item["context_tag"] = infer_context(combined)
    return item


def run_tagging(input_path: str, output_path: str) -> List[Dict]:
    """Tag all items."""
    with open(input_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        tag_item(item)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    # Print tag distribution
    comp_dist = {}
    skill_dist = {}
    ctx_dist = {}
    for item in items:
        c = item.get("competency_tag", "?")
        comp_dist[c] = comp_dist.get(c, 0) + 1
        s = item.get("skill_tag", "?")
        skill_dist[s] = skill_dist.get(s, 0) + 1
        t = item.get("context_tag", "?")
        ctx_dist[t] = ctx_dist.get(t, 0) + 1

    print(f"Tagged {len(items)} items")
    print("\nCompetency distribution:")
    for k, v in sorted(comp_dist.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print("\nTop 10 skill tags:")
    for k, v in sorted(skill_dist.items(), key=lambda x: -x[1])[:10]:
        print(f"  {k}: {v}")
    print("\nContext distribution:")
    for k, v in sorted(ctx_dist.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print(f"\nSaved to: {output_path}")

    return items


if __name__ == "__main__":
    input_p = os.path.join(PROJECT_ROOT, "data", "corpus_validated.json")
    output_p = os.path.join(PROJECT_ROOT, "data", "corpus_tagged.json")
    run_tagging(input_p, output_p)
