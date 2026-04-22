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


class TestSearchWiki(unittest.TestCase):
    """Tests for p2p-wiki-search."""

    def test_help(self):
        code, stdout, stderr = run_script("p2p-wiki-search", "search_wiki.py", ["--help"])
        self.assertEqual(code, 0)
        self.assertIn("Search the P2P Foundation Wiki", stdout)

    def test_missing_query(self):
        code, stdout, stderr = run_script("p2p-wiki-search", "search_wiki.py", [])
        self.assertNotEqual(code, 0)


class TestReadArticle(unittest.TestCase):
    """Tests for p2p-wiki-read."""

    def test_help(self):
        code, stdout, stderr = run_script("p2p-wiki-read", "read_article.py", ["--help"])
        self.assertEqual(code, 0)
        self.assertIn("Read full article content", stdout)

    def test_missing_title(self):
        code, stdout, stderr = run_script("p2p-wiki-read", "read_article.py", [])
        self.assertNotEqual(code, 0)


class TestBrowseCategories(unittest.TestCase):
    """Tests for p2p-wiki-categories."""

    def test_help(self):
        code, stdout, stderr = run_script("p2p-wiki-categories", "browse_categories.py", ["--help"])
        self.assertEqual(code, 0)
        self.assertIn("Browse P2P Foundation Wiki categories", stdout)

    def test_missing_action(self):
        code, stdout, stderr = run_script("p2p-wiki-categories", "browse_categories.py", [])
        self.assertNotEqual(code, 0)


class TestExploreWiki(unittest.TestCase):
    """Tests for p2p-wiki-explore."""

    def test_help(self):
        code, stdout, stderr = run_script("p2p-wiki-explore", "explore_wiki.py", ["--help"])
        self.assertEqual(code, 0)
        self.assertIn("Discover random, recent, or trending", stdout)

    def test_missing_action(self):
        code, stdout, stderr = run_script("p2p-wiki-explore", "explore_wiki.py", [])
        self.assertNotEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
