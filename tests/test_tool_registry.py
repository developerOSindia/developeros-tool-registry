"""
Unit tests for DeveloperOS Tool Registry integrity and business logic.
"""

import sys
import unittest
from pathlib import Path

REGISTRY_ROOT = Path(__file__).resolve().parent.parent
if str(REGISTRY_ROOT) not in sys.path:
    sys.path.insert(0, str(REGISTRY_ROOT))

from registry_manager import ToolRegistryManager


class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.mgr = ToolRegistryManager()

    def test_registry_validity(self):
        report = self.mgr.validate()
        self.assertTrue(report["valid"], f"Registry validation failed: {report['errors']}")
        self.assertGreaterEqual(report["tool_count"], 20)

    def test_unique_ids_and_slugs(self):
        ids = [t["id"] for t in self.mgr.tools]
        slugs = [t["seo_slug"] for t in self.mgr.tools]
        self.assertEqual(len(ids), len(set(ids)), "All tool IDs must be strictly unique")
        self.assertEqual(len(slugs), len(set(slugs)), "All SEO slugs must be strictly unique")

    def test_zero_fabricated_urls(self):
        """Rule: Only publish a live link once verified. Staged tools must have null live_url."""
        for tool in self.mgr.tools:
            if tool["availability_status"] == "staged_local":
                self.assertIsNone(
                    tool["live_url"],
                    f"Tool {tool['id']} is marked 'staged_local' but has non-null live_url: {tool['live_url']}"
                )

    def test_query_by_id_and_slug(self):
        tool = self.mgr.get_tool_by_id("tool-json-formatter")
        self.assertIsNotNone(tool)
        self.assertEqual(tool["name"], "JSON Formatter & Prettifier")

        tool_slug = self.mgr.get_tool_by_slug("json-formatter")
        self.assertIsNotNone(tool_slug)
        self.assertEqual(tool_slug["id"], "tool-json-formatter")

    def test_categories(self):
        cats = self.mgr.get_categories()
        self.assertIn("Formatters & Converters", cats)
        self.assertIn("Security & Encoders", cats)
        self.assertIn("Text & Inspection", cats)
        self.assertIn("Web & Design Tools", cats)


if __name__ == "__main__":
    unittest.main()
