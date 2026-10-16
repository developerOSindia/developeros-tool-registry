"""
DeveloperOS Tool Registry Manager
Pure Python, standard-library implementation for validating, querying,
and managing the DeveloperOS centralized tool registry.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

REGISTRY_DIR = Path(__file__).resolve().parent
REGISTRY_FILE = REGISTRY_DIR / "registry.json"
SCHEMA_FILE = REGISTRY_DIR / "schema.json"


class ToolRegistryManager:
    def __init__(self, registry_path: Path = REGISTRY_FILE):
        self.registry_path = registry_path
        self._data: Optional[Dict[str, Any]] = None
        self.reload()

    def reload(self):
        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {"version": "1.0.0", "tools": []}

    @property
    def tools(self) -> List[Dict[str, Any]]:
        return self._data.get("tools", [])

    def get_tool_by_id(self, tool_id: str) -> Optional[Dict[str, Any]]:
        for tool in self.tools:
            if tool.get("id") == tool_id:
                return tool
        return None

    def get_tool_by_slug(self, seo_slug: str) -> Optional[Dict[str, Any]]:
        for tool in self.tools:
            if tool.get("seo_slug") == seo_slug:
                return tool
        return None

    def list_tools(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        results = []
        for t in self.tools:
            if category and t.get("category") != category:
                continue
            if status and t.get("availability_status") != status:
                continue
            if search_query:
                q = search_query.lower()
                matched = (
                    q in t.get("name", "").lower()
                    or q in t.get("short_description", "").lower()
                    or q in t.get("category", "").lower()
                )
                if not matched:
                    continue
            results.append(t)
        return results

    def get_categories(self) -> List[str]:
        cats = sorted(list({t.get("category") for t in self.tools if t.get("category")}))
        return cats

    def validate(self) -> Dict[str, Any]:
        """Validates all entries against business and safety constraints."""
        errors: List[str] = []
        warnings: List[str] = []

        seen_ids = set()
        seen_slugs = set()

        for idx, tool in enumerate(self.tools, start=1):
            t_id = tool.get("id")
            if not t_id or not t_id.startswith("tool-"):
                errors.append(f"Tool #{idx}: Invalid or missing id '{t_id}'. Must start with 'tool-'.")
            elif t_id in seen_ids:
                errors.append(f"Tool #{idx}: Duplicate tool id '{t_id}'.")
            seen_ids.add(t_id)

            slug = tool.get("seo_slug")
            if not slug or not slug.islower():
                errors.append(f"Tool {t_id}: Invalid SEO slug '{slug}'. Must be lowercase hyphenated.")
            elif slug in seen_slugs:
                errors.append(f"Tool {t_id}: Duplicate SEO slug '{slug}'.")
            seen_slugs.add(slug)

            # Safety Rule: Only publish a live link once verified
            live_url = tool.get("live_url")
            status = tool.get("availability_status")
            if status == "verified_live" and not live_url:
                errors.append(f"Tool {t_id}: Status is 'verified_live' but live_url is null or empty.")
            if live_url and status != "verified_live":
                warnings.append(f"Tool {t_id}: Has live_url '{live_url}' but status is '{status}'. Must be verified.")

            # Required fields
            req_fields = [
                "name", "category", "short_description", "long_description",
                "parent_suite", "repository_url", "framework",
                "hosting_provider", "privacy_classification", "version"
            ]
            for field in req_fields:
                if not tool.get(field):
                    errors.append(f"Tool {t_id}: Missing required field '{field}'.")

        return {
            "valid": len(errors) == 0,
            "tool_count": len(self.tools),
            "errors": errors,
            "warnings": warnings
        }


# Singleton instance
registry_manager = ToolRegistryManager()

if __name__ == "__main__":
    report = registry_manager.validate()
    print(f"Registry Validation: {'PASS' if report['valid'] else 'FAIL'}")
    print(f"Total Tools Cataloged: {report['tool_count']}")
    if report["errors"]:
        print("Errors:")
        for err in report["errors"]:
            print(f"  - {err}")
    if report["warnings"]:
        print("Warnings:")
        for warn in report["warnings"]:
            print(f"  - {warn}")
