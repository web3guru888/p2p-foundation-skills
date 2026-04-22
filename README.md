# 🌐 P2P Foundation Skills

**Portable AI agent skills for the [P2P Foundation Wiki](https://wiki.p2pfoundation.net/) — use from any AI coding assistant.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/web3guru888/p2p-foundation-skills.svg)](https://github.com/web3guru888/p2p-foundation-skills/issues)
[![No API Key](https://img.shields.io/badge/API%20Key-not%20needed-brightgreen.svg)](#-quick-start)

Give your AI coding agent (Claude Code, Codex, Copilot, Cursor, Gemini CLI) the ability to search, read, browse, and explore the **P2P Foundation Wiki** — the world's largest knowledge base on peer-to-peer, commons, and decentralized topics. Each skill is a self-contained Python script plus a `SKILL.md` that any AI coding agent can read and act on immediately.

> **No API key required!** The P2P Foundation Wiki is fully public. Just clone and go.

---

## 🏛️ What is the P2P Foundation?

The [P2P Foundation](https://p2pfoundation.net/) (Peer-to-Peer Foundation) is a global research organization focused on studying, documenting, and promoting peer-to-peer dynamics in society. Their **wiki** is an extraordinary resource:

- **45,000+ articles** covering peer production, commons governance, cooperative economics, decentralized technology, open source, and more
- **25,000+ content pages** with deep analysis of P2P concepts, projects, and thinkers
- **150,000+ edits** contributed by 980+ editors since 2006
- Founded by **Michel Bauwens** — one of the foremost thinkers on P2P and the commons

Topics span blockchain governance, platform cooperativism, digital commons, gift economy, degrowth, community currencies, open hardware, and far more.

---

## 📦 Skills

| Skill | What it does | Key script |
|-------|-------------|-----------|
| [`p2p-wiki-search`](skills/p2p-wiki-search/) | Search 45K+ wiki articles by keyword | `search_wiki.py` |
| [`p2p-wiki-read`](skills/p2p-wiki-read/) | Read full article content (text or wikitext) | `read_article.py` |
| [`p2p-wiki-categories`](skills/p2p-wiki-categories/) | Browse articles by category and subcategory | `browse_categories.py` |
| [`p2p-wiki-explore`](skills/p2p-wiki-explore/) | Discover random articles, recent changes, and stats | `explore_wiki.py` |

---

## ⚡ Quick Start

### 1. Clone this repo

```bash
git clone https://github.com/web3guru888/p2p-foundation-skills.git
cd p2p-foundation-skills
pip install requests   # only dependency
```

**No API key needed!** The P2P Foundation Wiki is public.

### 2. Run a skill

```bash
# Search for articles on commons-based peer production
python3 skills/p2p-wiki-search/scripts/search_wiki.py --query "commons-based peer production" --limit 5

# Read a full article
python3 skills/p2p-wiki-read/scripts/read_article.py --title "Michel Bauwens"

# Browse categories
python3 skills/p2p-wiki-categories/scripts/browse_categories.py --category "Peer Production"

# Get random articles for discovery
python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --random 5

# Wiki statistics
python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --stats
```

All scripts output JSON to stdout. Errors go to stderr. Exit code 0 on success, 1 on failure.

---

## 🤖 Using With AI Coding Assistants

These skills follow the [SKILL.md specification](https://github.com/anthropics/skill-md-spec). Each skill directory contains a `SKILL.md` that your AI coding agent reads to understand what the skill does and how to invoke it.

**Example — Claude Code / Cursor / Copilot:**

```
You: "What does the P2P Foundation say about platform cooperativism?"

Agent reads: skills/p2p-wiki-search/SKILL.md
Agent runs:  python3 skills/p2p-wiki-search/scripts/search_wiki.py --query "platform cooperativism" --limit 5
Agent reads: skills/p2p-wiki-read/SKILL.md  
Agent runs:  python3 skills/p2p-wiki-read/scripts/read_article.py --title "Platform Cooperativism"
Agent:       "According to the P2P Foundation Wiki, platform cooperativism is..."
```

**To enable these skills**, point your AI coding agent at this repo (clone it into your project or reference the SKILL.md files).

### Supported AI Coding Assistants

| Assistant | How to use |
|-----------|-----------|
| **Claude Code** | Clone repo into your project. Claude reads SKILL.md files automatically. |
| **GitHub Copilot** | Reference SKILL.md in your workspace context. |
| **Cursor** | Add skills directory to your project. Cursor discovers SKILL.md files. |
| **Codex** | Include SKILL.md files in your agent instructions. |
| **Gemini CLI** | Point to SKILL.md files as tool definitions. |

---

## 🔧 How It Works

All skills use the **MediaWiki API** — the same API that powers Wikipedia. The P2P Foundation Wiki runs MediaWiki 1.40.4 with CirrusSearch.

```
Base URL: https://wiki.p2pfoundation.net/api.php
Auth:     None required (public wiki)
Format:   JSON
```

### API Endpoints Used

| Endpoint | Used by |
|----------|---------|
| `action=query&list=search` | p2p-wiki-search |
| `action=parse` | p2p-wiki-read (text mode) |
| `action=query&prop=revisions` | p2p-wiki-read (wikitext mode) |
| `action=query&list=allcategories` | p2p-wiki-categories |
| `action=query&list=categorymembers` | p2p-wiki-categories |
| `action=query&list=random` | p2p-wiki-explore |
| `action=query&list=recentchanges` | p2p-wiki-explore |
| `action=query&meta=siteinfo` | p2p-wiki-explore |

---

## 📁 Repo Structure

```
p2p-foundation-skills/
├── README.md                           # This file
├── AGENTS.md                           # Instructions for AI agents
├── CONTRIBUTING.md                     # How to contribute
├── LICENSE                             # Apache 2.0
├── skills/
│   ├── p2p-wiki-search/
│   │   ├── SKILL.md                    # Skill definition
│   │   └── scripts/
│   │       └── search_wiki.py          # Search articles by keyword
│   ├── p2p-wiki-read/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── read_article.py         # Read full article content
│   ├── p2p-wiki-categories/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── browse_categories.py    # Browse by category
│   └── p2p-wiki-explore/
│       ├── SKILL.md
│       └── scripts/
│           └── explore_wiki.py         # Random, recent, stats
├── examples/
│   └── README.md                       # Worked examples
├── docs/
│   └── mediawiki-api.md                # MediaWiki API reference
└── tests/
    ├── test_unit.py                    # Unit tests
    └── README.md                       # Test instructions
```

---

## 🔗 Links

- **P2P Foundation Wiki**: https://wiki.p2pfoundation.net/
- **P2P Foundation**: https://p2pfoundation.net/
- **P2P Foundation Blog**: https://blog.p2pfoundation.net/
- **MediaWiki API Docs**: https://www.mediawiki.org/wiki/API:Main_page
- **SKILL.md Specification**: https://github.com/anthropics/skill-md-spec

---

## 📄 License

Apache 2.0 — see [LICENSE](LICENSE).

P2P Foundation Wiki content is available under [Creative Commons Attribution-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
