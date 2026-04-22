# Instructions for AI Agents Working on This Repo

## What This Repo Is

This is a collection of **portable agent skills** (SKILL.md format) that enable AI coding agents to interact with the [P2P Foundation Wiki](https://wiki.p2pfoundation.net/) — the world's largest knowledge base on peer-to-peer, commons, and decentralized topics.

## Repo Structure

- `skills/` — Each subdirectory is a self-contained skill
  - `SKILL.md` — The skill definition (what you read to learn the skill)
  - `scripts/` — Runnable Python scripts (only dependency: `requests`)
- `examples/` — Worked examples showing real outputs
- `docs/` — Reference documentation (MediaWiki API)
- `tests/` — Unit tests

## How to Add a New Skill

1. Create `skills/<skill-name>/SKILL.md` with proper frontmatter
2. Create `skills/<skill-name>/scripts/<script>.py` — self-contained, CLI-ready
3. Add entry to the table in `README.md`
4. Add tests in `tests/`

## Skill Script Requirements

- **Self-contained**: Only needs `requests` library (stdlib + requests)
- **CLI interface**: Uses `argparse`, runnable from command line
- **JSON output**: Results go to stdout as valid JSON
- **Error handling**: Logs/errors go to stderr, exit code 1 on failure
- **No API key**: The P2P Foundation Wiki is public — no authentication needed
- **Apache 2.0 license header**

## SKILL.md Format

Follow the [SKILL.md specification](https://github.com/anthropics/skill-md-spec):

```yaml
---
name: skill-name
description: >
  One-paragraph description of what this skill does.
  Include trigger phrases and key capabilities.
license: Apache-2.0
compatibility: Python 3.8+, network access
metadata:
  version: "1.0.0"
  author: "web3guru888"
  last-updated: "2026-04-22"
allowed-tools: Read Bash(python3 *) Bash(pip install requests)
---
```

## Key Technical Facts

- **Base URL**: `https://wiki.p2pfoundation.net/api.php`
- **Auth**: None required (public wiki)
- **MediaWiki version**: 1.40.4 with CirrusSearch
- **Content**: 45,074 pages, 25,473 articles, 150,137 edits
- **API format**: Standard MediaWiki API (same as Wikipedia)

## Testing

```bash
pip install requests
python3 skills/p2p-wiki-search/scripts/search_wiki.py --query "commons" --limit 3
python3 skills/p2p-wiki-read/scripts/read_article.py --title "Michel Bauwens" --sections
python3 skills/p2p-wiki-categories/scripts/browse_categories.py --list --limit 5
python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --stats
```

All scripts should output valid JSON on success and exit 0, or print an error to stderr and exit 1.
