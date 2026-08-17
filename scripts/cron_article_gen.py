#!/usr/bin/env python3
"""Pick the next keyword for article generation."""
import json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import NICHE_KEYWORDS, SEARCH_INTENTS
from article_store import load_index

def make_slug(kw):
    s = kw.lower().replace(" ", "-")
    s = "".join(c for c in s if c.isalnum() or c == "-")
    return s[:60]

def main():
    idx = load_index()
    slugs = idx.get("published_slugs", set())
    if isinstance(slugs, list): slugs = set(slugs)
    
    # Find unused keywords, cycle if all used
    available = [kw for kw in NICHE_KEYWORDS if make_slug(kw) not in slugs]
    if not available:
        available = NICHE_KEYWORDS[:]
        idx["published_slugs"] = set()
        from article_store import save_index
        save_index(idx)
    
    kw = random.choice(available)
    intent = random.choice(list(SEARCH_INTENTS.keys()))
    cat = random.choice(["tech", "productivity", "office", "lifestyle"])
    
    result = {
        "keyword": kw,
        "slug": make_slug(kw),
        "intent": intent,
        "category": cat,
        "title": f"{SEARCH_INTENTS[intent]['angle']}：{kw}"
    }
    json.dump(result, sys.stdout, ensure_ascii=False)

if __name__ == "__main__":
    main()