#!/usr/bin/env python3
"""站点配置"""
import os, json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SITE_NAME = "工具精选指南"
SITE_TAGLINE = "实测推荐 · 真实评测 · 帮你选对产品"
SITE_URL = "https://toolpicks.keyinxiao.com"
AUTHOR = "工具精选团队"

CONTENT_DIR = BASE_DIR / "content"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"
ASSETS_DIR = BASE_DIR / "assets"

AFFILIATE_CONFIG = {
    "amazon_com": {"tag": "toolpicks08-20", "base": "https://www.amazon.com/dp/"},
    "amazon_cn": {"tag": "toolpicks-23", "base": "https://www.amazon.cn/dp/"},
}

NICHE_KEYWORDS = [
    "best budget laptop", "top wireless mouse", "noise cancelling headphones",
    "best mechanical keyboard", "home office setup",
    "best monitor for work", "ergonomic chair review", "best webcam 2025",
    "budget smartphone", "wireless earbuds review",
    "best portable charger", "SSD external drive", "best VPN service",
    "video editing laptop", "best drawing tablet",
    "smart home devices", "best wifi router", "air purifier review",
    "standing desk review", "office chair budget",
    "best budget monitor", "mechanical keyboard budget", "best laptop backpack",
    "ultrawide monitor review", "budget gaming laptop",
    "best noise cancelling earbuds", "productivity tablet",
]

SEARCH_INTENTS = {
    "review": {"pattern": "{} review", "angle": "深度评测"},
    "best": {"pattern": "best {} 2025", "angle": "TOP推荐"},
    "budget": {"pattern": "best budget {}", "angle": "性价比之选"},
    "guide": {"pattern": "{} buying guide", "angle": "选购指南"},
}

try:
    SECRETS = json.loads(os.environ.get("SITE_SECRETS", "{}"))
except json.JSONDecodeError:
    SECRETS = {}