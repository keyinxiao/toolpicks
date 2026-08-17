#!/usr/bin/env python3
"""Build static site from article content."""
import json, sys
from pathlib import Path
from datetime import datetime

_script_dir = Path(__file__).resolve().parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))
from config import *

def build():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    
    idx_file = CONTENT_DIR / "index.json"
    if not idx_file.exists():
        print("No index yet")
        return
    with open(idx_file) as f:
        index = json.load(f)
    articles = sorted(index.get("articles", []), key=lambda a: a.get("date",""), reverse=True)
    
    # Render index page
    html = env.get_template("index.html").render(
        site_name=SITE_NAME, site_tagline=SITE_TAGLINE,
        year=datetime.now().year, url=SITE_URL,
        title="首页", description=SITE_TAGLINE,
        articles=[{"title":a["title"],"slug":a["slug"],"excerpt":a.get("excerpt",""),"date":a.get("date","")} for a in articles[:50]]
    )
    with open(OUTPUT_DIR / "index.html", "w") as f:
        f.write(html)
    
    # Render article pages
    for a in articles:
        af = CONTENT_DIR / f"{a['slug']}.json"
        if not af.exists(): continue
        with open(af) as f:
            data = json.load(f)
        html = env.get_template("article.html").render(
            site_name=SITE_NAME, site_tagline=SITE_TAGLINE,
            year=datetime.now().year, url=f"{SITE_URL}/{a['slug']}/",
            title=data["title"], description=data.get("excerpt",""),
            date=data.get("date",""), word_count=len(data.get("content","")),
            content=data.get("content",""),
        )
        (OUTPUT_DIR / a["slug"]).mkdir(exist_ok=True)
        with open(OUTPUT_DIR / a["slug"] / "index.html", "w") as f:
            f.write(html)
    
    # Render category pages
    for cat, slugs in index.get("categories", {}).items():
        cat_articles = [a for a in articles if a.get("category") == cat]
        html = env.get_template("index.html").render(
            site_name=SITE_NAME, site_tagline=SITE_TAGLINE,
            year=datetime.now().year, url=f"{SITE_URL}/categories/{cat}/",
            title=f"{cat} - {SITE_NAME}", description=f"{cat}分类文章",
            articles=[{"title":a["title"],"slug":a["slug"],"excerpt":a.get("excerpt",""),"date":a.get("date","")} for a in cat_articles]
        )
        cat_dir = OUTPUT_DIR / "categories" / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        with open(cat_dir / "index.html", "w") as f:
            f.write(html)
    
    print(f"Built: {len(articles)} articles, index, categories")

if __name__ == "__main__":
    build()