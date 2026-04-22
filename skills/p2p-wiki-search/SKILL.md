---
name: p2p-wiki-search
description: >
  Search the P2P Foundation Wiki for articles on peer-to-peer, commons, open-source,
  and decentralized topics. Returns titles, snippets, page IDs, and timestamps.
  Use when asked to find information about P2P concepts, commons-based peer production,
  cooperative economics, digital commons, or related topics. No API key needed.
license: Apache-2.0
compatibility: Python 3.8+, network access
metadata:
  version: "1.0.0"
  author: "web3guru888"
  last-updated: "2026-04-22"
allowed-tools: Read Bash(python3 *) Bash(pip install cloudscraper requests) Bash(pip install -r requirements.txt)
---

# P2P Wiki Search

## Overview

Full-text search across the P2P Foundation Wiki's 45,000+ articles covering peer-to-peer theory, commons governance, decentralized technology, cooperative economics, and open-source movements.

## When to Use

- User asks about P2P concepts, commons, or decentralization
- User asks "what does the P2P Foundation say about..."
- User asks to find articles on cooperative economics, digital commons, or open source
- You need background research on peer production, sharing economy, or community governance

## Prerequisites

- Python 3.8+ with `requests`
- **No API key needed** — the P2P Foundation Wiki is public

## Quick Steps

### 1. Search by keyword
```bash
python3 scripts/search_wiki.py --query "commons-based peer production" --limit 10
```

### 2. Paginate results
```bash
python3 scripts/search_wiki.py --query "blockchain governance" --limit 10 --offset 10
```

### 3. Parse results
```json
{
  "status": "success",
  "query": "commons-based peer production",
  "total": 850,
  "returned": 10,
  "offset": 0,
  "results": [
    {
      "title": "Commons-Based Peer Production",
      "page_id": 1234,
      "snippet": "Commons-based peer production is a term coined by...",
      "word_count": 5420,
      "size_bytes": 32100,
      "timestamp": "2024-03-15T10:30:00Z",
      "url": "https://wiki.p2pfoundation.net/Commons-Based_Peer_Production"
    }
  ]
}
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--query` / `-q` | Yes | Search query (e.g., "digital commons") |
| `--limit` / `-l` | No | Max results, 1-50 (default: 10) |
| `--offset` / `-o` | No | Pagination offset (default: 0) |

## How It Works

Uses the MediaWiki Search API:
```
GET https://wiki.p2pfoundation.net/api.php?action=query&list=search&srsearch={query}&srlimit={limit}&format=json
```

The wiki runs MediaWiki 1.40.4 with CirrusSearch, providing full-text search with relevance ranking across all 45,000+ content pages.

## Edge Cases

- **No results**: Try broader terms — the wiki uses specific P2P/commons terminology
- **HTML in snippets**: Snippets are automatically cleaned of HTML tags
- **Large result sets**: Use `--offset` to paginate through thousands of results

## References

- [P2P Foundation Wiki](https://wiki.p2pfoundation.net/)
- [MediaWiki Search API](https://www.mediawiki.org/wiki/API:Search)
