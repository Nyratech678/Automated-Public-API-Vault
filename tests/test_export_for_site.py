import json
import tempfile
import unittest
from pathlib import Path

from src.writer import API, export_for_site


class ExportForSiteTests(unittest.TestCase):
    def test_export_for_site_writes_expected_json_files(self):
        categorized = {
            "Security": [
                API(
                    name="API One",
                    description="desc",
                    language="Python",
                    stars=10,
                    updated_at="2026-01-01",
                    archived=False,
                    url="https://example.com/api-one",
                )
            ],
            "Data": [
                API(
                    name="API Two",
                    description="desc2",
                    language="Go",
                    stars=20,
                    updated_at="2026-02-01",
                    archived=True,
                    url="https://example.com/api-two",
                )
            ],
        }

        with tempfile.TemporaryDirectory() as tmp:
            export_for_site(categorized, tmp)
            apis = json.loads(Path(tmp, "apis.json").read_text(encoding="utf-8"))
            categories = json.loads(
                Path(tmp, "categories.json").read_text(encoding="utf-8")
            )

        self.assertEqual(len(apis), 2)
        self.assertEqual(apis[0]["name"], "API One")
        self.assertEqual(apis[1]["archived"], True)
        self.assertEqual(
            categories,
            {
                "categories": [
                    {"name": "Security", "count": 1},
                    {"name": "Data", "count": 1},
                ]
            },
        )


if __name__ == "__main__":
    unittest.main()
