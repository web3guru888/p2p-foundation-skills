#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 web3guru888
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
read_article.py — Read full article content from the P2P Foundation Wiki.

Fetches and extracts clean text from any wiki article. Supports both
parsed HTML (cleaned to plain text) and raw wikitext output formats.

Usage:
    python3 read_article.py --title "Commons-Based Peer Production"
    python3 read_article.py --title "Michel Bauwens" --format wikitext
    python3 read_article.py --title "Blockchain" --sections

Requirements:
    - cloudscraper (preferred) or requests library
      pip install cloudscraper   # handles Cloudflare-protected wiki
      pip install requests       # fallback (may get 403 if Cloudflare is active)
    - No API key needed — the P2P Foundation Wiki is public

Output:
    JSON to stdout: {"status": "success", "title": "...", "content": "...", ...}
"""

import argparse
import json
import re
import sys

# Prefer cloudscraper (handles Cloudflare); fall back to plain requests.
try:
    import cloudscraper
    _SESSION = cloudscraper.create_scraper()
except ImportError:
    try:
        import requests
        _SESSION = requests.Session()
    except ImportError:
        print(
            json.dumps({
                "status": "error",
                "error": (
                    "Neither cloudscraper nor requests is installed. "
                    "Run: pip install cloudscraper"
                ),
            }),
            file=sys.stdout,
        )
        sys.exit(1)


API_URL = "https://wiki.p2pfoundation.net/api.php"


def log(msg):
    """Print log message to stderr."""
    print("[p2p-wiki-read] {}".format(msg), file=sys.stderr)


def strip_html(html):
    """Remove HTML tags and clean up whitespace."""
    # Remove script and style elements
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Convert common elements to text markers
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</?p[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<h([1-6])[^>]*>(.*?)</h\1>", r"\n\n## \2\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li[^>]*>", "\n- ", text, flags=re.IGNORECASE)
    # Remove remaining tags
    text = re.sub(r"<[^>]+>", "", text)
    # Clean up HTML entities
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#039;", "'")
    text = text.replace("&nbsp;", " ")
    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" +", " ", text)
    return text.strip()


def read_article_parsed(title):
    """Read article using the parse API (returns cleaned HTML → plain text).

    Args:
        title: Article title (e.g., "Commons-Based Peer Production").

    Returns:
        dict with article content and metadata.
    """
    params = {
        "action": "parse",
        "page": title,
        "prop": "text|categories|sections|displaytitle",
        "disabletoc": "true",
        "format": "json",
    }

    log("Fetching parsed article: {}".format(title))

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {
            "status": "error",
            "error": data["error"].get("info", "Unknown API error"),
            "code": data["error"].get("code", ""),
        }

    parse = data.get("parse", {})
    html_content = parse.get("text", {}).get("*", "")
    plain_text = strip_html(html_content)

    categories = [cat.get("*", "") for cat in parse.get("categories", [])]
    sections = [
        {"level": int(s.get("level", 2)), "title": s.get("line", ""), "index": s.get("index", "")}
        for s in parse.get("sections", [])
    ]

    # Strip HTML from displaytitle (MediaWiki wraps it in <span> tags)
    display_title = re.sub(r"<[^>]+>", "", parse.get("displaytitle", title)).strip()

    return {
        "status": "success",
        "title": display_title,
        "page_id": parse.get("pageid", 0),
        "format": "text",
        "content": plain_text,
        "content_length": len(plain_text),
        "sections": sections,
        "categories": categories,
        "url": "https://wiki.p2pfoundation.net/{}".format(title.replace(" ", "_")),
    }


def read_article_wikitext(title):
    """Read article as raw wikitext.

    Args:
        title: Article title.

    Returns:
        dict with raw wikitext content.
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "revisions|categories",
        "rvprop": "content|timestamp|user",
        "rvslots": "main",
        "cllimit": "50",
        "format": "json",
    }

    log("Fetching wikitext for: {}".format(title))

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {"status": "error", "error": data["error"].get("info", "Unknown API error")}

    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return {"status": "error", "error": "No pages returned"}

    page_id = list(pages.keys())[0]
    if page_id == "-1":
        return {
            "status": "error",
            "error": "Article not found: {}".format(title),
            "suggestion": "Check the title spelling. Titles are case-sensitive.",
        }

    page = pages[page_id]
    revisions = page.get("revisions", [])
    if not revisions:
        return {"status": "error", "error": "No revisions found for article"}

    rev = revisions[0]
    # MediaWiki 1.32+ uses slots
    slots = rev.get("slots", {})
    if slots:
        content = slots.get("main", {}).get("*", "")
    else:
        content = rev.get("*", "")

    categories = [cat.get("title", "").replace("Category:", "") for cat in page.get("categories", [])]

    return {
        "status": "success",
        "title": page.get("title", title),
        "page_id": int(page_id),
        "format": "wikitext",
        "content": content,
        "content_length": len(content),
        "last_editor": rev.get("user", ""),
        "last_edited": rev.get("timestamp", ""),
        "categories": categories,
        "url": "https://wiki.p2pfoundation.net/{}".format(title.replace(" ", "_")),
    }


def list_sections(title):
    """List only the section headings of an article.

    Args:
        title: Article title.

    Returns:
        dict with section list.
    """
    params = {
        "action": "parse",
        "page": title,
        "prop": "sections|displaytitle",
        "format": "json",
    }

    log("Listing sections for: {}".format(title))

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {"status": "error", "error": data["error"].get("info", "Unknown API error")}

    parse = data.get("parse", {})
    sections = [
        {"level": int(s.get("level", 2)), "title": s.get("line", ""), "number": s.get("number", "")}
        for s in parse.get("sections", [])
    ]

    # Strip HTML from displaytitle (MediaWiki wraps it in <span> tags)
    display_title = re.sub(r"<[^>]+>", "", parse.get("displaytitle", title)).strip()

    return {
        "status": "success",
        "title": display_title,
        "page_id": parse.get("pageid", 0),
        "section_count": len(sections),
        "sections": sections,
        "url": "https://wiki.p2pfoundation.net/{}".format(title.replace(" ", "_")),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Read full article content from the P2P Foundation Wiki."
    )
    parser.add_argument(
        "--title", "-t",
        required=True,
        help="Article title (e.g., 'Commons-Based Peer Production')"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "wikitext"],
        default="text",
        help="Output format: 'text' (cleaned plain text, default) or 'wikitext' (raw wiki markup)"
    )
    parser.add_argument(
        "--sections", "-s",
        action="store_true",
        help="List only section headings (no content)"
    )

    args = parser.parse_args()

    if args.sections:
        result = list_sections(args.title)
    elif args.format == "wikitext":
        result = read_article_wikitext(args.title)
    else:
        result = read_article_parsed(args.title)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
