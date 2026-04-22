# Examples

Worked examples showing real CLI invocations and outputs from the P2P Foundation Skills.

## Quick Examples

### Search for articles
```bash
$ python3 skills/p2p-wiki-search/scripts/search_wiki.py --query "platform cooperativism" --limit 3

{
  "status": "success",
  "query": "platform cooperativism",
  "total": 127,
  "returned": 3,
  "offset": 0,
  "results": [
    {
      "title": "Platform Cooperativism",
      "page_id": 28451,
      "snippet": "Platform cooperativism is a growing movement that...",
      "word_count": 3200,
      "url": "https://wiki.p2pfoundation.net/Platform_Cooperativism"
    }
  ]
}
```

### Read an article
```bash
$ python3 skills/p2p-wiki-read/scripts/read_article.py --title "Michel Bauwens" --sections

{
  "status": "success",
  "title": "Michel Bauwens",
  "section_count": 12,
  "sections": [
    {"level": 2, "title": "Biography", "number": "1"},
    {"level": 2, "title": "Key Concepts", "number": "2"},
    {"level": 2, "title": "Publications", "number": "3"}
  ]
}
```

### Get wiki statistics
```bash
$ python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --stats

{
  "status": "success",
  "mode": "statistics",
  "site": {
    "name": "P2P Foundation",
    "generator": "MediaWiki 1.40.4"
  },
  "statistics": {
    "pages": 45074,
    "articles": 25473,
    "edits": 150137,
    "users": 981,
    "active_users": 4
  }
}
```

### Discover random articles
```bash
$ python3 skills/p2p-wiki-explore/scripts/explore_wiki.py --random 3

{
  "status": "success",
  "mode": "random",
  "returned": 3,
  "articles": [
    {"title": "Self Managed Open Network Innovation", "url": "https://wiki.p2pfoundation.net/..."},
    {"title": "Commons Podcast Series", "url": "https://wiki.p2pfoundation.net/..."},
    {"title": "People's Cloud", "url": "https://wiki.p2pfoundation.net/..."}
  ]
}
```
