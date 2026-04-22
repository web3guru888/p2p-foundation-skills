# Contributing to P2P Foundation Skills

Thank you for helping grow the library of P2P Foundation Wiki skills! This guide explains how to add new skills, run existing scripts locally, write tests, and submit a pull request.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Adding a New Skill](#adding-a-new-skill)
3. [Script Requirements](#script-requirements)
4. [Running Locally](#running-locally)
5. [Tests](#tests)
6. [Code Style](#code-style)
7. [Pull Request Guidelines](#pull-request-guidelines)

---

## Project Structure

```
skills/
└── <skill-name>/
    ├── SKILL.md          # Skill definition (required)
    └── scripts/
        └── <script>.py   # Self-contained CLI script (required)
examples/                  # Worked examples showing real outputs
docs/                      # Cross-skill reference documentation
tests/
└── test_unit.py           # Unit tests
```

Every skill lives in its own directory under `skills/`. The directory name becomes the skill's canonical identifier (e.g., `p2p-wiki-search`).

---

## Adding a New Skill

### 1. Create the skill directory

```bash
mkdir -p skills/<skill-name>/scripts
```

Naming convention: `p2p-wiki-<action>` using kebab-case, e.g. `p2p-wiki-search`, `p2p-wiki-read`.

### 2. Write the SKILL.md

Follow the [SKILL.md specification](https://github.com/anthropics/skill-md-spec). This is what AI coding agents read to discover and use the skill.

### 3. Write the Python script

See [Script Requirements](#script-requirements) below.

### 4. Add an entry to README.md

Add a row to the **Skills** table in `README.md`.

### 5. Add tests

Add test functions to `tests/test_unit.py`.

---

## Script Requirements

Every script under `skills/*/scripts/` must follow these rules:

### Dependencies
- **Only `requests` + Python stdlib.** No other third-party packages.
- Python 3.8+ compatible (no walrus operator, no match statements, no `str | None`)

### CLI interface
- Use `argparse` for argument parsing
- Include `--help` text for every argument
- Runnable directly: `python3 skills/foo/scripts/foo.py --arg value`

### Output
- **Stdout**: Valid JSON on success
- **Stderr**: Human-readable log/error messages
- **Exit code**: 0 on success, 1 on failure

### No authentication
The P2P Foundation Wiki is public — no API key or login needed.

### License header
Include the Apache 2.0 header at the top:

```python
# Copyright 2026 web3guru888
#
# Licensed under the Apache License, Version 2.0 ...
```

---

## Running Locally

```bash
git clone https://github.com/web3guru888/p2p-foundation-skills.git
cd p2p-foundation-skills
pip install requests

# Run any script
python3 skills/p2p-wiki-search/scripts/search_wiki.py --query "digital commons" --limit 5
python3 skills/p2p-wiki-read/scripts/read_article.py --title "Michel Bauwens"
python3 skills/p2p-wiki-categories/scripts/browse_categories.py --list
python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --stats
```

---

## Tests

```bash
pip install requests
python3 -m pytest tests/ -v
```

---

## Code Style

- **PEP 8** compliant
- **Python 3.8 compatibility** (minimum supported version)
- **Type hints** encouraged but not required
- **Docstrings** for all public functions

---

## Pull Request Guidelines

1. **Test your changes** — run the affected scripts locally
2. **Update README.md** if you add a skill
3. **One concern per PR** — separate bug fixes from new features
4. **Use conventional commits**: `feat:`, `fix:`, `docs:`

---

## Questions?

Open an issue at [github.com/web3guru888/p2p-foundation-skills/issues](https://github.com/web3guru888/p2p-foundation-skills/issues).
