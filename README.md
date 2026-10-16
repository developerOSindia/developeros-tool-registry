# DeveloperOS Tool Registry (`developeros-tool-registry`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ecosystem: DeveloperOS](https://img.shields.io/badge/Ecosystem-DeveloperOS-6366f1.svg)](https://developeros.in)
[![Tools Directory](https://img.shields.io/badge/Tools%20Directory-Online-10b981.svg)](https://tools.developeros.in)
[![Privacy: Client--Side](https://img.shields.io/badge/Privacy-Zero--Storage-10b981.svg)](https://developeros.in/privacy)
[![CI](https://github.com/developerOSindia/developeros-tool-registry/actions/workflows/ci.yml/badge.svg)](https://github.com/developerOSindia/developeros-tool-registry/actions)

The single source of truth for all tools, applications, and suites in the DeveloperOS open-source ecosystem.

---

## 🖥️ Schema Overview

Every tool entry conforms strictly to [`schema.json`](schema.json) with 14 standardized fields:
- `id`: Unique identifier (e.g., `tool-json-formatter`)
- `name`: Human-readable display name
- `category`: Functional grouping
- `short_description`: One-line summary
- `long_description`: Exhaustive functional overview
- `parent_suite`: Parent suite metadata (`id`, `name`)
- `live_url`: Verified public deployment URL (or `null` if unverified/staged)
- `repository_url`: GitHub source link under `developerOSindia`
- `seo_slug`: URL slug for static SEO landing pages
- `framework`: Application framework (e.g., `Streamlit`, `Vanilla JS`)
- `hosting_provider`: e.g. `Streamlit Community Cloud`, `Cloudflare Pages`
- `availability_status`: `staged_local`, `verified_live`, `in_development`
- `privacy_classification`: `client_side_ephemeral`, `zero_storage_client`
- `version`: Semantic version
- `last_verified_date`: Verification timestamp or `null`

---

## 🔒 Safety & Deployment Rules

> [!IMPORTANT]
> **Zero Fabrication Policy**: A `live_url` is only published once an application has been deployed to public infrastructure and its URL verified live. Staged tools must maintain a `null` live link.

---

## 🚀 Usage

```python
from registry_manager import registry_manager

# Query all formatters
formatters = registry_manager.list_tools(category="Formatters & Converters")

# Query tool by SEO slug
tool = registry_manager.get_tool_by_slug("json-formatter")
print(tool["name"], tool["repository_url"])
```

---

## 🧪 Automated Testing

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 🏷️ Recommended GitHub Topics

`json-schema` `tool-registry` `developer-tools` `api-metadata` `developeros` `open-source`

---

## 📜 License & Ecosystem

Licensed under [MIT](LICENSE).
- **Main Website**: [https://developeros.in](https://developeros.in)
- **Central Tools Directory**: [https://tools.developeros.in](https://tools.developeros.in)
- **GitHub Organization**: [https://github.com/developerOSindia](https://github.com/developerOSindia)
