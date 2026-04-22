# Tests

## Running Tests

### Unit tests (no network required)
```bash
pip install requests
python3 -m pytest tests/test_unit.py -v
```

### Manual integration tests
```bash
# These hit the live P2P Foundation Wiki API
python3 skills/p2p-wiki-search/scripts/search_wiki.py --query "commons" --limit 3
python3 skills/p2p-wiki-read/scripts/read_article.py --title "Commons" --sections
python3 skills/p2p-wiki-categories/scripts/browse_categories.py --list --limit 3
python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --stats
```

All scripts should output valid JSON and exit 0 on success.
