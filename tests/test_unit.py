#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 web3guru888
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Unit tests for P2P Foundation Skills.

Tests script CLI interface, argument parsing, and output format
without making network calls (where possible).
"""

import json
import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

SKILLS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "skills")


def run_script(skill_name, script_name, args):
    """Run a skill script and return (returncode, stdout, stderr)."""
    script_path = os.path.join(SKILLS_DIR, skill_name, "scripts", script_name)
    result = subprocess.run(
        [sys.executable, script_path] + args,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout, result.stderr


# ---------------------------------------------------------------------------
# CLI / argument-parsing tests (no network)
# ---------------------------------------------------------------------------

class TestSearchWiki(unittest.TestCase):
    """CLI tests for p2p-wiki-search."""

    def test_help(self):
        code, stdout, stderr = run_script("p2p-wiki-search", "search_wiki.py", ["--help"])
        self.assertEqual(code, 0)
        self.assertIn("Search the P2P Foundation Wiki", stdout)

    def test_missing_query(self):
        code, stdout, stderr = run_script("p2p-wiki-search", "search_wiki.py", [])
        self.assertNotEqual(code, 0)


class TestReadArticle(unittest.TestCase):
    """CLI tests for p2p-wiki-read."""

    def test_help(self):
        code, stdout, stderr = run_script("p2p-wiki-read", "read_article.py", ["--help"])
        self.assertEqual(code, 0)
        self.assertIn("Read full article content", stdout)

    def test_missing_title(self):
        code, stdout, stderr = run_script("p2p-wiki-read", "read_article.py", [])
        self.assertNotEqual(code, 0)


class TestBrowseCategories(unittest.TestCase):
    """CLI tests for p2p-wiki-categories."""

    def test_help(self):
        code, stdout, stderr = run_script("p2p-wiki-categories", "browse_categories.py", ["--help"])
        self.assertEqual(code, 0)
        self.assertIn("Browse P2P Foundation Wiki categories", stdout)

    def test_missing_action(self):
        code, stdout, stderr = run_script("p2p-wiki-categories", "browse_categories.py", [])
        self.assertNotEqual(code, 0)

    def test_empty_category_rejected(self):
        code, stdout, stderr = run_script(
            "p2p-wiki-categories", "browse_categories.py", ["--category", ""]
        )
        self.assertNotEqual(code, 0)
        data = json.loads(stdout)
        self.assertEqual(data["status"], "error")
        self.assertIn("empty", data["error"].lower())


class TestExploreWiki(unittest.TestCase):
    """CLI tests for p2p-wiki-explore."""

    def test_help(self):
        code, stdout, stderr = run_script("p2p-wiki-explore", "explore_wiki.py", ["--help"])
        self.assertEqual(code, 0)
        self.assertIn("Discover random, recent, or trending", stdout)

    def test_missing_action(self):
        code, stdout, stderr = run_script("p2p-wiki-explore", "explore_wiki.py", [])
        self.assertNotEqual(code, 0)


# ---------------------------------------------------------------------------
# Mock-based JSON output structure tests (no network)
# ---------------------------------------------------------------------------

def _make_mock_response(payload):
    """Return a MagicMock that mimics a requests/cloudscraper Response."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = payload
    return mock_resp


class TestSearchWikiOutputStructure(unittest.TestCase):
    """Mock-based output structure tests for p2p-wiki-search."""

    def _import_module(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "search_wiki",
            os.path.join(SKILLS_DIR, "p2p-wiki-search", "scripts", "search_wiki.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_output_structure(self):
        """search_wiki() returns correct keys with mocked API response."""
        fake_api_response = {
            "query": {
                "searchinfo": {"totalhits": 42},
                "search": [
                    {
                        "title": "Commons",
                        "pageid": 1001,
                        "snippet": "The <b>commons</b> is shared.",
                        "wordcount": 500,
                        "size": 8000,
                        "timestamp": "2026-01-01T00:00:00Z",
                    },
                    {
                        "title": "Peer Production",
                        "pageid": 1002,
                        "snippet": "Peer production is a form of <b>collaboration</b>.",
                        "wordcount": 300,
                        "size": 5000,
                        "timestamp": "2026-01-02T00:00:00Z",
                    },
                ],
            }
        }

        mod = self._import_module()
        mock_resp = _make_mock_response(fake_api_response)

        with patch.object(mod, "_SESSION") as mock_session:
            mock_session.get.return_value = mock_resp
            result = mod.search_wiki("commons", limit=2)

        self.assertEqual(result["status"], "success")
        self.assertIn("query", result)
        self.assertIn("total", result)
        self.assertIn("returned", result)
        self.assertIn("results", result)
        self.assertEqual(result["total"], 42)
        self.assertEqual(result["returned"], 2)
        self.assertEqual(len(result["results"]), 2)

        # Check individual result keys
        for item in result["results"]:
            for key in ("title", "page_id", "snippet", "word_count", "size_bytes",
                        "timestamp", "url"):
                self.assertIn(key, item, msg="Missing key '{}' in result item".format(key))

        # Snippet should have HTML stripped
        self.assertNotIn("<b>", result["results"][0]["snippet"])


class TestReadArticleOutputStructure(unittest.TestCase):
    """Mock-based output structure tests for p2p-wiki-read."""

    def _import_module(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "read_article",
            os.path.join(SKILLS_DIR, "p2p-wiki-read", "scripts", "read_article.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_output_structure(self):
        """read_article_parsed() returns correct keys with mocked API response."""
        fake_api_response = {
            "parse": {
                "title": "Michel Bauwens",
                "pageid": 3417,
                "displaytitle": '<span class="mw-page-title-main">Michel Bauwens</span>',
                "text": {"*": "<p>Michel Bauwens is a Belgian writer.</p>"},
                "sections": [
                    {"level": "2", "line": "Biography", "index": "1", "number": "1"},
                ],
                "categories": [
                    {"*": "P2P_theorists"},
                    {"*": "Belgian_people"},
                ],
            }
        }

        mod = self._import_module()
        mock_resp = _make_mock_response(fake_api_response)

        with patch.object(mod, "_SESSION") as mock_session:
            mock_session.get.return_value = mock_resp
            result = mod.read_article_parsed("Michel Bauwens")

        self.assertEqual(result["status"], "success")
        for key in ("title", "page_id", "format", "content", "content_length",
                    "sections", "categories", "url"):
            self.assertIn(key, result, msg="Missing key '{}'".format(key))

        # Title must be plain text, not HTML
        self.assertNotIn("<span", result["title"])
        self.assertEqual(result["title"], "Michel Bauwens")
        self.assertEqual(result["page_id"], 3417)
        self.assertEqual(result["format"], "text")
        self.assertIsInstance(result["sections"], list)
        self.assertIsInstance(result["categories"], list)


class TestBrowseCategoriesOutputStructure(unittest.TestCase):
    """Mock-based output structure tests for p2p-wiki-categories."""

    def _import_module(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "browse_categories",
            os.path.join(SKILLS_DIR, "p2p-wiki-categories", "scripts", "browse_categories.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_output_structure(self):
        """get_category_members() returns correct keys with mocked API response."""
        fake_api_response = {
            "query": {
                "categorymembers": [
                    {
                        "title": "Commons-Based Peer Production",
                        "type": "page",
                        "timestamp": "2026-01-01T00:00:00Z",
                    },
                    {
                        "title": "Peer Governance",
                        "type": "page",
                        "timestamp": "2026-01-02T00:00:00Z",
                    },
                ]
            }
        }

        mod = self._import_module()
        mock_resp = _make_mock_response(fake_api_response)

        with patch.object(mod, "_SESSION") as mock_session:
            mock_session.get.return_value = mock_resp
            result = mod.get_category_members("Peerproduction", limit=2)

        self.assertEqual(result["status"], "success")
        for key in ("category", "member_type", "returned", "has_more", "members"):
            self.assertIn(key, result, msg="Missing key '{}'".format(key))

        self.assertEqual(result["returned"], 2)
        self.assertIsInstance(result["members"], list)

        for item in result["members"]:
            for key in ("title", "type", "timestamp", "url"):
                self.assertIn(key, item, msg="Missing key '{}' in member".format(key))


class TestExploreWikiStatsStructure(unittest.TestCase):
    """Mock-based output structure tests for p2p-wiki-explore --stats."""

    def _import_module(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "explore_wiki",
            os.path.join(SKILLS_DIR, "p2p-wiki-explore", "scripts", "explore_wiki.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_stats_structure(self):
        """get_stats() returns correct keys with mocked API response."""
        fake_api_response = {
            "query": {
                "general": {
                    "sitename": "P2P Foundation Wiki",
                    "generator": "MediaWiki 1.40.4",
                    "base": "https://wiki.p2pfoundation.net/Main_Page",
                },
                "statistics": {
                    "pages": 45074,
                    "articles": 25473,
                    "edits": 150137,
                    "images": 1200,
                    "users": 981,
                    "activeusers": 4,
                    "admins": 18,
                },
            }
        }

        mod = self._import_module()
        mock_resp = _make_mock_response(fake_api_response)

        with patch.object(mod, "_SESSION") as mock_session:
            mock_session.get.return_value = mock_resp
            result = mod.get_statistics()

        self.assertEqual(result["status"], "success")
        for key in ("mode", "site", "statistics"):
            self.assertIn(key, result, msg="Missing key '{}'".format(key))

        self.assertEqual(result["mode"], "statistics")
        for stat_key in ("pages", "articles", "edits", "users", "active_users", "admins"):
            self.assertIn(stat_key, result["statistics"],
                          msg="Missing stat key '{}'".format(stat_key))

        self.assertEqual(result["statistics"]["pages"], 45074)
        self.assertEqual(result["site"]["name"], "P2P Foundation Wiki")


if __name__ == "__main__":
    unittest.main()
