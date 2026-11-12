import unittest
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


class PodcastConfigTest(unittest.TestCase):
    def test_no_malformed_urls(self):
        """Ensure no double-h URL typos like hhttps:// exist."""
        for py_file in SCRIPTS.glob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            self.assertNotIn("hhttps://", content, f"Found malformed 'hhttps://' in {py_file.name}")

    def test_refresh_token_validation(self):
        """Ensure refresh_token fails informatively when REFRESH_TOKEN is missing."""
        import os
        from unittest.mock import patch

        with patch.dict(os.environ, {}, clear=True):
            import podcast
            with self.assertRaises(ValueError) as ctx:
                podcast.refresh_token()
            self.assertIn("REFRESH_TOKEN", str(ctx.exception))

    def test_notion_helper_env_validation(self):
        """Ensure NotionHelper fails informatively when required env vars are missing."""
        import os
        from unittest.mock import patch
        from notion_helper import NotionHelper

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as ctx:
                NotionHelper()
            self.assertIn("NOTION_TOKEN", str(ctx.exception))

        with patch.dict(os.environ, {"NOTION_TOKEN": "mock_token"}, clear=True):
            with self.assertRaises(ValueError) as ctx:
                NotionHelper()
            self.assertIn("NOTION_PAGE", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
