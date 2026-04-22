---
name: p2p-wiki-explore
description: >
  Discover random, recent, or trending content on the P2P Foundation Wiki.
  Get random articles for serendipitous learning, view recent edits, or
  check wiki-wide statistics. No API key needed.
license: Apache-2.0
compatibility: Python 3.8+, network access
metadata:
  version: "1.0.0"
  author: "web3guru888"
  last-updated: "2026-04-22"
allowed-tools: Read Bash(python3 *) Bash(pip install requests)
---

# P2P Wiki Explore

## Overview

Explore the P2P Foundation Wiki through random article discovery, the recent changes feed, and site-wide statistics. Great for learning about new P2P concepts serendipitously, tracking wiki activity, or understanding the scope of the knowledge base.

## When to Use

- User asks "show me something interesting about P2P"
- User wants to discover random P2P concepts or articles
- User asks about recent wiki activity or edits
- You need to understand the wiki's scope (article count, editor count, etc.)

## Prerequisites

- Python 3.8+ with `requests`
- **No API key needed** — the P2P Foundation Wiki is public

## Quick Steps

### 1. Get random articles
```bash
python3 scripts/explore_wiki.py --random 5
```

### 2. Get recent changes
```bash
python3 scripts/explore_wiki.py --recent 20
```

### 3. Filter recent changes
```bash
python3 scripts/explore_wiki.py --recent 10 --type new
```

### 4. Get wiki statistics
```bash
python3 scripts/explore_wiki.py --stats
```

### 5. Parse results
```json
{
  "status": "success",
  "mode": "statistics",
  "site": {
    "name": "P2P Foundation",
    "base_url": "https://wiki.p2pfoundation.net/Main_Page",
    "generator": "MediaWiki 1.40.4",
    "language": "en"
  },
  "statistics": {
    "pages": 45074,
    "articles": 25473,
    "edits": 150137,
    "images": 1242,
    "users": 981,
    "active_users": 4,
    "admins": 18
  }
}
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--random` / `-r` | One of three | Get N random articles (1-50) |
| `--recent` | One of three | Get N recent changes (1-500) |
| `--stats` | One of three | Get wiki-wide statistics |
| `--type` | No | Filter recent changes: "edit", "new", or "log" |

## How It Works

Uses three MediaWiki API endpoints:
- **Random**: `api.php?action=query&list=random&rnnamespace=0`
- **Recent changes**: `api.php?action=query&list=recentchanges`
- **Statistics**: `api.php?action=query&meta=siteinfo&siprop=statistics`

## Edge Cases

- **Low activity**: The wiki may have few recent changes (currently ~4 active users)
- **Random is truly random**: Results differ every call, cannot be paginated
- **Recent changes include bots**: Automated edits may appear in the feed

## References

- [P2P Foundation Wiki](https://wiki.p2pfoundation.net/)
- [MediaWiki Random API](https://www.mediawiki.org/wiki/API:Random)
- [MediaWiki RecentChanges API](https://www.mediawiki.org/wiki/API:RecentChanges)
