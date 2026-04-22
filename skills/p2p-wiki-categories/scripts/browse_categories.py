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
browse_categories.py — Browse P2P Foundation Wiki categories.

List all categories, view articles within a category, or find subcategories.
Enables structured navigation of the wiki's 45,000+ articles by topic.

Usage:
    python3 browse_categories.py --list
    python3 browse_categories.py --list --prefix "Block"
    python3 browse_categories.py --category "Peer Production"
    python3 browse_categories.py --category "Commons" --type subcat

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
    print("[p2p-wiki-categories] {}".format(msg), file=sys.stderr)


def list_categories(limit=50, prefix=None):
    """List all categories on the wiki.

    Args:
        limit: Max categories to return (1-500).
        prefix: Optional prefix filter (e.g., "Block" → "Blockchain", "Block chain"...).

    Returns:
        dict with category list.
    """
    limit = max(1, min(500, limit))

    params = {
        "action": "query",
        "list": "allcategories",
        "aclimit": limit,
        "acprop": "size",
        "format": "json",
    }

    if prefix:
        params["acprefix"] = prefix

    log("Listing categories (limit={}, prefix={})".format(limit, prefix))

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {"status": "error", "error": data["error"].get("info", "Unknown API error")}

    categories = []
    for cat in data.get("query", {}).get("allcategories", []):
        categories.append({
            "name": cat.get("*", ""),
            "pages": cat.get("pages", 0),
            "subcats": cat.get("subcats", 0),
            "files": cat.get("files", 0),
            "size": cat.get("size", 0),
        })

    has_more = "continue" in data

    return {
        "status": "success",
        "returned": len(categories),
        "has_more": has_more,
        "prefix": prefix,
        "categories": categories,
    }


def get_category_members(category, limit=50, member_type="page"):
    """Get articles or subcategories within a category.

    Args:
        category: Category name (without "Category:" prefix).
        limit: Max members to return (1-500).
        member_type: "page" for articles, "subcat" for subcategories, "all" for both.

    Returns:
        dict with category member list.
    """
    limit = max(1, min(500, limit))

    type_map = {"page": "page", "subcat": "subcat", "all": "page|subcat|file"}
    cm_type = type_map.get(member_type, "page")

    # Ensure proper prefix
    cat_title = category if category.startswith("Category:") else "Category:{}".format(category)

    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": cat_title,
        "cmlimit": limit,
        "cmtype": cm_type,
        "cmprop": "title|type|timestamp",
        "format": "json",
    }

    log("Getting members of {} (type={}, limit={})".format(cat_title, member_type, limit))

    try:
        resp = _SESSION.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "error": "API request failed: {}".format(str(e))}

    data = resp.json()

    if "error" in data:
        return {"status": "error", "error": data["error"].get("info", "Unknown API error")}

    members = []
    for member in data.get("query", {}).get("categorymembers", []):
        title = member.get("title", "")
        m_type = member.get("type", "page")
        members.append({
            "title": title.replace("Category:", "") if m_type == "subcat" else title,
            "type": m_type,
            "timestamp": member.get("timestamp", ""),
            "url": "https://wiki.p2pfoundation.net/{}".format(title.replace(" ", "_")),
        })

    has_more = "continue" in data

    return {
        "status": "success",
        "category": category,
        "member_type": member_type,
        "returned": len(members),
        "has_more": has_more,
        "members": members,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Browse P2P Foundation Wiki categories."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list",
        action="store_true",
        help="List all categories"
    )
    group.add_argument(
        "--category", "-c",
        help="Get members of a specific category (e.g., 'Peer Production')"
    )

    parser.add_argument(
        "--prefix", "-p",
        help="Filter categories by prefix (used with --list)"
    )
    parser.add_argument(
        "--type",
        choices=["page", "subcat", "all"],
        default="page",
        help="Type of category members to return (used with --category, default: page)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=50,
        help="Max results to return (1-500, default: 50)"
    )

    args = parser.parse_args()

    # Validate category name is not empty
    if args.category is not None and not args.category.strip():
        error = {"status": "error", "error": "Category name cannot be empty."}
        print(json.dumps(error, indent=2))
        sys.exit(1)

    if args.list:
        result = list_categories(limit=args.limit, prefix=args.prefix)
    else:
        result = get_category_members(args.category, limit=args.limit, member_type=args.type)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
