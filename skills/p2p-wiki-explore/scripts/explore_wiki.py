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
explore_wiki.py — Discover random, recent, or trending content on the P2P Foundation Wiki.

Explore the wiki through random article discovery, recent changes feed,
and site-wide statistics. Great for serendipitous learning about P2P topics.

Usage:
    python3 explore_wiki.py --random 5
    python3 explore_wiki.py --recent 20
    python3 explore_wiki.py --stats

Requirements:
    - cloudscraper (preferred) or requests library
      pip install cloudscraper   # handles Cloudflare-protected wiki
      pip install requests       # fallback (may get 403 if Cloudflare is active)
    - No API key needed — the P2P Foundation Wiki is public

Output:
    JSON to stdout: {"status": "success", ...}
"""

import argparse
import json
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
    print("[p2p-wiki-explore] {}".format(msg), file=sys.stderr)


def get_random_articles(count=5):
    """Get random articles from the wiki.

    Args:
        count: Number of random articles (1-50).

    Returns:
        dict with random article list.
    """
    count = max(1, min(50, count))

    params = {
        "action": "query",
        "list": "random",
        "rnlimit": count,
        "rnnamespace": "0",  # Main namespace only (articles)
        "format": "json",
    }

    log("Getting {} random articles".format(count))

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {"status": "error", "error": data["error"].get("info", "Unknown API error")}

    articles = []
    for item in data.get("query", {}).get("random", []):
        title = item.get("title", "")
        articles.append({
            "title": title,
            "page_id": item.get("id", 0),
            "url": "https://wiki.p2pfoundation.net/{}".format(title.replace(" ", "_")),
        })

    return {
        "status": "success",
        "mode": "random",
        "returned": len(articles),
        "articles": articles,
    }


def get_recent_changes(limit=20, change_type=None):
    """Get recent changes to the wiki.

    Args:
        limit: Max changes to return (1-500).
        change_type: Filter by type: "edit", "new", "log" (optional).

    Returns:
        dict with recent changes list.
    """
    limit = max(1, min(500, limit))

    params = {
        "action": "query",
        "list": "recentchanges",
        "rclimit": limit,
        "rcprop": "title|timestamp|user|comment|sizes|flags",
        "rcnamespace": "0",  # Main namespace only
        "format": "json",
    }

    if change_type:
        params["rctype"] = change_type

    log("Getting {} recent changes".format(limit))

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {"status": "error", "error": data["error"].get("info", "Unknown API error")}

    changes = []
    for item in data.get("query", {}).get("recentchanges", []):
        title = item.get("title", "")
        old_len = item.get("oldlen", 0)
        new_len = item.get("newlen", 0)
        changes.append({
            "title": title,
            "timestamp": item.get("timestamp", ""),
            "user": item.get("user", ""),
            "comment": item.get("comment", ""),
            "type": item.get("type", ""),
            "old_size": old_len,
            "new_size": new_len,
            "size_diff": new_len - old_len,
            "minor": "minor" in item,
            "url": "https://wiki.p2pfoundation.net/{}".format(title.replace(" ", "_")),
        })

    return {
        "status": "success",
        "mode": "recent",
        "returned": len(changes),
        "changes": changes,
    }


def get_statistics():
    """Get wiki-wide statistics.

    Returns:
        dict with wiki statistics.
    """
    params = {
        "action": "query",
        "meta": "siteinfo",
        "siprop": "statistics|general",
        "format": "json",
    }

    log("Getting wiki statistics")

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {"status": "error", "error": data["error"].get("info", "Unknown API error")}

    query = data.get("query", {})
    stats = query.get("statistics", {})
    general = query.get("general", {})

    return {
        "status": "success",
        "mode": "statistics",
        "site": {
            "name": general.get("sitename", ""),
            "base_url": general.get("base", ""),
            "generator": general.get("generator", ""),
            "language": general.get("lang", ""),
        },
        "statistics": {
            "pages": stats.get("pages", 0),
            "articles": stats.get("articles", 0),
            "edits": stats.get("edits", 0),
            "images": stats.get("images", 0),
            "users": stats.get("users", 0),
            "active_users": stats.get("activeusers", 0),
            "admins": stats.get("admins", 0),
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Discover random, recent, or trending content on the P2P Foundation Wiki."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--random", "-r",
        type=int,
        metavar="N",
        help="Get N random articles (1-50)"
    )
    group.add_argument(
        "--recent",
        type=int,
        metavar="N",
        help="Get N recent changes (1-500)"
    )
    group.add_argument(
        "--stats",
        action="store_true",
        help="Get wiki-wide statistics"
    )

    parser.add_argument(
        "--type",
        choices=["edit", "new", "log"],
        help="Filter recent changes by type (used with --recent)"
    )

    args = parser.parse_args()

    if args.random is not None:
        result = get_random_articles(args.random)
    elif args.recent is not None:
        result = get_recent_changes(args.recent, change_type=args.type)
    else:
        result = get_statistics()

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
