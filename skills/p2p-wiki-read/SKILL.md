---
name: p2p-wiki-read
description: >
  Read full article content from the P2P Foundation Wiki. Fetches and extracts
  clean text or raw wikitext from any article. Can also list section headings.
  Use when asked to read, summarize, or extract information from a specific
  P2P Foundation Wiki article. No API key needed.
license: Apache-2.0
compatibility: Python 3.8+, network access
metadata:
  version: "1.0.0"
  author: "web3guru888"
  last-updated: "2026-04-22"
allowed-tools: Read Bash(python3 *) Bash(pip install cloudscraper requests) Bash(pip install -r requirements.txt)
---

# P2P Wiki Read

## Overview

Fetch and read the full content of any article on the P2P Foundation Wiki. Supports clean plain text output (default) and raw wikitext. Can also list section headings for quick navigation of long articles.

## When to Use

- User asks to read or summarize a specific P2P Foundation article
- You found an article via `p2p-wiki-search` and need the full content
- User asks "what does the P2P Foundation Wiki say about X"
- You need to extract detailed information from a wiki page

## Prerequisites

- Python 3.8+ with `requests`
- **No API key needed** — the P2P Foundation Wiki is public

## Quick Steps

### 1. Read an article (cleaned text)
```bash
python3 scripts/read_article.py --title "Commons-Based Peer Production"
```

### 2. Read as raw wikitext
```bash
python3 scripts/read_article.py --title "Michel Bauwens" --format wikitext
```

### 3. List sections only
```bash
python3 scripts/read_article.py --title "Blockchain" --sections
```

### 4. Parse results
```json
{
  "status": "success",
  "title": "Commons-Based Peer Production",
  "page_id": 1234,
  "format": "text",
  "content": "Commons-based peer production is a term coined by Harvard Law School professor...",
  "content_length": 15420,
  "sections": [
    {"level": 2, "title": "Definition", "index": "1"},
    {"level": 2, "title": "History", "index": "2"}
  ],
  "categories": ["Peer Production", "Commons"],
  "url": "https://wiki.p2pfoundation.net/Commons-Based_Peer_Production"
}
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--title` / `-t` | Yes | Article title (case-sensitive, e.g., "Michel Bauwens") |
| `--format` / `-f` | No | Output: "text" (default) or "wikitext" |
| `--sections` / `-s` | No | List only section headings (no content) |

## How It Works

- **Text mode** (default): Uses the MediaWiki Parse API to get rendered HTML, then strips tags to clean plain text. Also returns sections and categories.
- **Wikitext mode**: Uses the Revisions API to get raw wiki markup. Also returns last editor and edit timestamp.
- **Sections mode**: Uses the Parse API to return only section headings with levels.

## Edge Cases

- **Article not found**: Returns error with suggestion to check spelling (titles are case-sensitive)
- **Very long articles**: Content can be 50KB+; consider using `--sections` first to identify relevant parts
- **Redirects**: The API follows redirects automatically
- **Special characters in titles**: Use proper URL encoding (the script handles this)

## References

- [P2P Foundation Wiki](https://wiki.p2pfoundation.net/)
- [MediaWiki Parse API](https://www.mediawiki.org/wiki/API:Parsing_wikitext)
