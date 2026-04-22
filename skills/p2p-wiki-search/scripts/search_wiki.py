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
search_wiki.py — Search the P2P Foundation Wiki by keyword.

Uses the MediaWiki API to perform full-text search across 45,000+ articles
on peer-to-peer, commons, and open-source topics.

Usage:
    python3 search_wiki.py --query "commons-based peer production"
    python3 search_wiki.py --query "blockchain governance" --limit 20
    python3 search_wiki.py --query "Michel Bauwens" --offset 10

Requirements:
    - cloudscraper (preferred) or requests library
      pip install cloudscraper   # handles Cloudflare-protected wiki
      pip install requests       # fallback (may get 403 if Cloudflare is active)
    - No API key needed — the P2P Foundation Wiki is public

Output:
    JSON to stdout: {"status": "success", "query": "...", "total": N, "results": [...]}
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
    print("[p2p-wiki-search] {}".format(msg), file=sys.stderr)


def search_wiki(query, limit=10, offset=0):
    """Search the P2P Foundation Wiki using the MediaWiki search API.

    Args:
        query: Search term(s).
        limit: Max results to return (1-50).
        offset: Result offset for pagination.

    Returns:
        dict with status, query, total, returned, offset, and results list.
    """
    limit = max(1, min(50, limit))
    offset = max(0, offset)

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "sroffset": offset,
        "srinfo": "totalhits",
        "srprop": "snippet|timestamp|wordcount|size",
        "format": "json",
    }

    log("Searching for: {} (limit={}, offset={})".format(query, limit, offset))

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {"status": "error", "error": data["error"].get("info", "Unknown API error")}

    search_results = data.get("query", {}).get("search", [])
    total_hits = data.get("query", {}).get("searchinfo", {}).get("totalhits", 0)

    results = []
    for item in search_results:
        # Strip HTML tags from snippet
        snippet = item.get("snippet", "")
        snippet = re.sub(r"<[^>]+>", "", snippet)

        results.append({
            "title": item.get("title", ""),
            "page_id": item.get("pageid", 0),
            "snippet": snippet,
            "word_count": item.get("wordcount", 0),
            "size_bytes": item.get("size", 0),
            "timestamp": item.get("timestamp", ""),
            "url": "https://wiki.p2pfoundation.net/{}".format(
                item.get("title", "").replace(" ", "_")
            ),
        })

    return {
        "status": "success",
        "query": query,
        "total": total_hits,
        "returned": len(results),
        "offset": offset,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Search the P2P Foundation Wiki by keyword."
    )
    parser.add_argument(
        "--query", "-q",
        required=True,
        help="Search query (e.g., 'commons-based peer production')"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="Max results to return (1-50, default: 10)"
    )
    parser.add_argument(
        "--offset", "-o",
        type=int,
        default=0,
        help="Result offset for pagination (default: 0)"
    )

    args = parser.parse_args()
    result = search_wiki(args.query, args.limit, args.offset)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
