---
name: p2p-wiki-categories
description: >
  Browse and navigate P2P Foundation Wiki categories. List all categories,
  view articles within a category, or find subcategories. Enables structured
  exploration of 45,000+ articles by topic. No API key needed.
license: Apache-2.0
compatibility: Python 3.8+, network access
metadata:
  version: "1.0.0"
  author: "web3guru888"
  last-updated: "2026-04-22"
allowed-tools: Read Bash(python3 *) Bash(pip install requests)
---

# P2P Wiki Categories

## Overview

Navigate the P2P Foundation Wiki's category system to discover articles organized by topic — from "Peer Production" and "Commons" to "Blockchain" and "Cooperative Economics". List all categories, browse articles in a specific category, or find subcategories.

## When to Use

- User wants to explore P2P topics by category
- User asks "what topics does the P2P Foundation cover?"
- You need to find all articles on a specific theme (e.g., all blockchain articles)
- You want to understand how P2P concepts are organized

## Prerequisites

- Python 3.8+ with `requests`
- **No API key needed** — the P2P Foundation Wiki is public

## Quick Steps

### 1. List all categories
```bash
python3 scripts/browse_categories.py --list --limit 20
```

### 2. Filter categories by prefix
```bash
python3 scripts/browse_categories.py --list --prefix "Block"
```

### 3. Get articles in a category
```bash
python3 scripts/browse_categories.py --category "Peer Production"
```

### 4. Get subcategories
```bash
python3 scripts/browse_categories.py --category "Commons" --type subcat
```

### 5. Parse results
```json
{
  "status": "success",
  "category": "Peer Production",
  "member_type": "page",
  "returned": 50,
  "has_more": true,
  "members": [
    {
      "title": "Commons-Based Peer Production",
      "type": "page",
      "timestamp": "2024-03-15T10:30:00Z",
      "url": "https://wiki.p2pfoundation.net/Commons-Based_Peer_Production"
    }
  ]
}
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--list` | One of `--list` or `--category` | List all categories |
| `--category` / `-c` | One of `--list` or `--category` | Get members of a category |
| `--prefix` / `-p` | No | Filter categories by prefix (with `--list`) |
| `--type` | No | Member type: "page" (default), "subcat", or "all" |
| `--limit` / `-l` | No | Max results, 1-500 (default: 50) |

## How It Works

Uses the MediaWiki Category APIs:
- **List categories**: `api.php?action=query&list=allcategories`
- **Category members**: `api.php?action=query&list=categorymembers&cmtitle=Category:{name}`

## Edge Cases

- **Empty categories**: Some categories exist but have no articles
- **Large categories**: Use `has_more` to know if pagination is needed
- **Case sensitivity**: Category names are case-sensitive

## References

- [P2P Foundation Wiki](https://wiki.p2pfoundation.net/)
- [MediaWiki Categories API](https://www.mediawiki.org/wiki/API:Allcategories)
