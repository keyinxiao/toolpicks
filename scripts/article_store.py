#!/usr/bin/env python3
"""文章存储：管理已发布文章索引"""
import json, os, sys
from pathlib import Path
from datetime import datetime

# Ensure parent dir is on path for config import
_script_dir = Path(__file__).resolve().parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))
from config import CONTENT_DIR

INDEX_FILE = CONTENT_DIR / "index.json"

def load_index():
    if INDEX_FILE.exists():
        with open(INDEX_FILE) as f:
            return json.load(f)
    return {"articles": [], "published_slugs": set(), "categories": {}}

def save_index(idx):
    idx["published_slugs"] = list(idx["published_slugs"])
    for k in list(idx["categories"].keys()):
        idx["categories"][k] = list(idx["categories"][k])
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    idx["published_slugs"] = set(idx["published_slugs"])
    for k in list(idx["categories"].keys()):
        idx["categories"][k] = set(idx["categories"][k])

def is_published(slug, idx):
    return slug in idx.get("published_slugs", set())

def add_article(title, slug, excerpt, content, category, affiliate_data=None):
    idx = load_index()
    idx["published_slugs"] = set(idx.get("published_slugs", []))
    for k in list(idx.get("categories", {}).keys()):
        idx["categories"][k] = set(idx["categories"][k])
    if "categories" not in idx:
        idx["categories"] = {}
    idx["articles"].append({
        "title": title, "slug": slug, "excerpt": excerpt,
        "category": category, "date": datetime.now().strftime("%Y-%m-%d"),
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "affiliate": affiliate_data or False,
    })
    idx["published_slugs"].add(slug)
    if category not in idx["categories"]:
        idx["categories"][category] = set()
    idx["categories"][category].add(slug)
    save_index(idx)
    article_file = CONTENT_DIR / f"{slug}.json"
    with open(article_file, "w") as f:
        json.dump({
            "title": title, "slug": slug, "date": idx["articles"][-1]["date"],
            "category": category, "content": content, "excerpt": excerpt,
            "affiliate": affiliate_data,
        }, f, ensure_ascii=False, indent=2)
    return slug