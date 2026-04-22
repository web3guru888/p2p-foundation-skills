# 🌐 P2P Foundation Skills

**Portable AI agent skills for the [P2P Foundation Wiki](https://wiki.p2pfoundation.net/) — use from any AI coding assistant.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/web3guru888/p2p-foundation-skills.svg)](https://github.com/web3guru888/p2p-foundation-skills/issues)
[![No API Key](https://img.shields.io/badge/API%20Key-not%20needed-brightgreen.svg)](#-quick-start)
[![Tests](https://img.shields.io/badge/tests-13%20passing-brightgreen.svg)](#-testing)

Give your AI coding agent (Claude Code, Codex, Copilot, Cursor, Gemini CLI) the ability to search, read, browse, and explore the **P2P Foundation Wiki** — the world's largest knowledge base on peer-to-peer, commons, and decentralized topics. Each skill is a self-contained Python script plus a `SKILL.md` that any AI coding agent can read and act on immediately.

> **No API key required!** The P2P Foundation Wiki is fully public.

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

### 1. Clone and install

```bash
git clone https://github.com/web3guru888/p2p-foundation-skills.git
cd p2p-foundation-skills
pip install -r requirements.txt
```

Or install dependencies directly:

```bash
pip install cloudscraper requests
```

> **Note:** The P2P Foundation Wiki is protected by **Cloudflare**. The scripts use
> [`cloudscraper`](https://github.com/VeNoMouS/cloudscraper) to handle this transparently.
> If `cloudscraper` is not installed, the scripts fall back to plain `requests` (which
> may receive `403 Forbidden` responses from Cloudflare). Always install `cloudscraper`
> for reliable operation.

### 2. Run a skill

```bash
# Search for articles on commons-based peer production
python3 skills/p2p-wiki-search/scripts/search_wiki.py \
    --query "commons-based peer production" --limit 5

# Read a full article
python3 skills/p2p-wiki-read/scripts/read_article.py \
    --title "Michel Bauwens"

# Browse category members
python3 skills/p2p-wiki-categories/scripts/browse_categories.py \
    --category "Peerproduction"

# Get random articles for discovery
python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --random 5

# Wiki-wide statistics
python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --stats
```

All scripts output **JSON to stdout**. Errors go to **stderr**. Exit code `0` on success, `1` on failure.

---

## 📋 JSON Output Examples

### `p2p-wiki-search --query "commons" --limit 2`

```json
{
  "status": "success",
  "query": "commons",
  "total": 8081,
  "returned": 2,
  "offset": 0,
  "results": [
    {
      "title": "Commons",
      "page_id": 1234,
      "snippet": "The commons is the cultural and natural resources accessible to all members of a society...",
      "word_count": 1200,
      "size_bytes": 18400,
      "timestamp": "2026-03-15T10:22:00Z",
      "url": "https://wiki.p2pfoundation.net/Commons"
    },
    {
      "title": "Digital Commons",
      "page_id": 5678,
      "snippet": "Digital commons are information and knowledge resources that are collectively created...",
      "word_count": 850,
      "size_bytes": 12300,
      "timestamp": "2026-02-10T08:44:00Z",
      "url": "https://wiki.p2pfoundation.net/Digital_Commons"
    }
  ]
}
```

### `p2p-wiki-explore --stats`

```json
{
  "status": "success",
  "mode": "statistics",
  "site": {
    "name": "P2P Foundation Wiki",
    "base_url": "https://wiki.p2pfoundation.net/Main_Page",
    "generator": "MediaWiki 1.40.4",
    "language": "en"
  },
  "statistics": {
    "pages": 45074,
    "articles": 25473,
    "edits": 150137,
    "images": 1200,
    "users": 981,
    "active_users": 4,
    "admins": 18
  }
}
```

---

## 🤖 Using With AI Coding Assistants

These skills follow the [SKILL.md specification](https://github.com/anthropics/skill-md-spec). Each skill directory contains a `SKILL.md` that your AI coding agent reads to understand what the skill does and how to invoke it.

**Example — Claude Code / Cursor / Copilot:**

```
You: "What does the P2P Foundation say about platform cooperativism?"

Agent reads: skills/p2p-wiki-search/SKILL.md
Agent runs:  python3 skills/p2p-wiki-search/scripts/search_wiki.py \
                 --query "platform cooperativism" --limit 5
Agent reads: skills/p2p-wiki-read/SKILL.md
Agent runs:  python3 skills/p2p-wiki-read/scripts/read_article.py \
                 --title "Platform Cooperativism"
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
Note:     Cloudflare-protected — use cloudscraper for reliable access
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

## 🧪 Testing

### Run unit tests

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v
```

The test suite includes **13 tests**:

- **CLI tests** — verify `--help`, required arguments, and invalid input handling for all 4 skills
- **Mock-based structure tests** — verify JSON output keys and values using mocked API responses (no network required)

```
tests/test_unit.py::TestSearchWiki::test_help                           PASSED
tests/test_unit.py::TestSearchWiki::test_missing_query                  PASSED
tests/test_unit.py::TestReadArticle::test_help                          PASSED
tests/test_unit.py::TestReadArticle::test_missing_title                 PASSED
tests/test_unit.py::TestBrowseCategories::test_help                     PASSED
tests/test_unit.py::TestBrowseCategories::test_missing_action           PASSED
tests/test_unit.py::TestBrowseCategories::test_empty_category_rejected  PASSED
tests/test_unit.py::TestExploreWiki::test_help                          PASSED
tests/test_unit.py::TestExploreWiki::test_missing_action                PASSED
tests/test_unit.py::TestSearchWikiOutputStructure::test_output_structure        PASSED
tests/test_unit.py::TestReadArticleOutputStructure::test_output_structure       PASSED
tests/test_unit.py::TestBrowseCategoriesOutputStructure::test_output_structure  PASSED
tests/test_unit.py::TestExploreWikiStatsStructure::test_stats_structure         PASSED

13 passed in ~3s
```

---

## 📁 Repo Structure

```
p2p-foundation-skills/
├── README.md                           # This file
├── AGENTS.md                           # Instructions for AI agents
├── CONTRIBUTING.md                     # How to contribute
├── LICENSE                             # Apache 2.0
├── requirements.txt                    # Python dependencies
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
    ├── test_unit.py                    # Unit + mock-based tests (13 tests)
    └── README.md                       # Test instructions
```

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Adding a new skill

Each skill follows the [SKILL.md specification](https://github.com/anthropics/skill-md-spec):

1. Create a directory: `skills/p2p-wiki-<name>/`
2. Add `SKILL.md` with valid YAML frontmatter (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`)
3. Add your Python script under `scripts/` — it must:
   - Output JSON to **stdout** only
   - Send logs/diagnostics to **stderr**
   - Exit `0` on success, `1` on error
   - Use `cloudscraper` (with `requests` fallback) for HTTP calls
   - Support `--help`
4. Add tests to `tests/test_unit.py`
5. Verify: `python3 -m pytest tests/ -v`

---

## 🔗 Links

- **P2P Foundation Wiki**: https://wiki.p2pfoundation.net/
- **P2P Foundation**: https://p2pfoundation.net/
- **P2P Foundation Blog**: https://blog.p2pfoundation.net/
- **MediaWiki API Docs**: https://www.mediawiki.org/wiki/API:Main_page
- **SKILL.md Specification**: https://github.com/anthropics/skill-md-spec
- **cloudscraper**: https://github.com/VeNoMouS/cloudscraper

---

## 📄 License

Apache 2.0 — see [LICENSE](LICENSE).

P2P Foundation Wiki content is available under [Creative Commons Attribution-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
