# MediaWiki API Reference

The P2P Foundation Wiki runs on **MediaWiki 1.40.4** with CirrusSearch. This document covers the API endpoints used by the skills in this repository.

## Base URL

```
https://wiki.p2pfoundation.net/api.php
```

All requests use `GET` with `format=json`. No authentication required.

## Endpoints

### Search (used by p2p-wiki-search)

```
GET /api.php?action=query&list=search&srsearch={query}&srlimit={limit}&sroffset={offset}&srinfo=totalhits&srprop=snippet|timestamp|wordcount|size&format=json
```

| Parameter | Description |
|-----------|-------------|
| `srsearch` | Search query string |
| `srlimit` | Max results (1-50) |
| `sroffset` | Pagination offset |
| `srinfo` | Include `totalhits` count |
| `srprop` | Properties to return |

### Parse (used by p2p-wiki-read)

```
GET /api.php?action=parse&page={title}&prop=text|categories|sections|displaytitle&format=json
```

Returns rendered HTML content which can be cleaned to plain text.

### Revisions (used by p2p-wiki-read)

```
GET /api.php?action=query&titles={title}&prop=revisions|categories&rvprop=content|timestamp|user&rvslots=main&format=json
```

Returns raw wikitext content of the latest revision.

### All Categories (used by p2p-wiki-categories)

```
GET /api.php?action=query&list=allcategories&aclimit={limit}&acprop=size&acprefix={prefix}&format=json
```

### Category Members (used by p2p-wiki-categories)

```
GET /api.php?action=query&list=categorymembers&cmtitle=Category:{name}&cmlimit={limit}&cmtype={type}&cmprop=title|type|timestamp&format=json
```

| `cmtype` value | Description |
|----------------|-------------|
| `page` | Articles only |
| `subcat` | Subcategories only |
| `page|subcat|file` | Everything |

### Random (used by p2p-wiki-explore)

```
GET /api.php?action=query&list=random&rnlimit={count}&rnnamespace=0&format=json
```

### Recent Changes (used by p2p-wiki-explore)

```
GET /api.php?action=query&list=recentchanges&rclimit={limit}&rcprop=title|timestamp|user|comment|sizes|flags&rcnamespace=0&format=json
```

### Site Info (used by p2p-wiki-explore)

```
GET /api.php?action=query&meta=siteinfo&siprop=statistics|general&format=json
```

## Rate Limiting

The P2P Foundation Wiki does not document explicit rate limits, but as a courtesy:
- Keep requests to a reasonable rate (1-2 per second)
- Use a descriptive User-Agent header
- Cache results when possible

## Further Reading

- [MediaWiki API Documentation](https://www.mediawiki.org/wiki/API:Main_page)
- [MediaWiki API Sandbox](https://wiki.p2pfoundation.net/Special:ApiSandbox)
