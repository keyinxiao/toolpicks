#!/usr/bin/env python3
"""Pick next keyword and output for article generation."""
import json, sys, random
from pathlib import Path

_script_dir = Path(__file__).resolve().parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))
from config import NICHE_KEYWORDS, SEARCH_INTENTS
from article_store import load_index, save_index

def make_slug(kw):
    s = kw.lower().replace(" ", "-").replace("--", "-")
    return "".join(c for c in s if c.isalnum() or c == "-")[:60]

def main():
    idx = load_index()
    slugs = idx.get("published_slugs", set())
    if isinstance(slugs, list): slugs = set(slugs)
    
    available = [kw for kw in NICHE_KEYWORDS if make_slug(kw) not in slugs]
    if not available:
        available = NICHE_KEYWORDS[:]
        idx["published_slugs"] = set()
        save_index(idx)
    
    kw = random.choice(available)
    intent = random.choice(list(SEARCH_INTENTS.keys()))
    cat = random.choice(["tech", "productivity", "office"])
    
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