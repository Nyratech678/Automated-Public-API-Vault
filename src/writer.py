import json
import logging
import os
from dataclasses import asdict, dataclass

logger = logging.getLogger(__name__)


@dataclass
class API:
    name: str
    description: str
    language: str
    stars: int
    updated_at: str
    archived: bool
    url: str


def write_readmes(categorized: dict[str, list[API]]) -> dict[str, int]:
    """
    Placeholder README writer that returns category counts.
    """
    return {category: len(apis) for category, apis in categorized.items()}


def export_for_site(categorized: dict[str, list[API]], output_dir: str = ".") -> None:
    """
    Generates apis.json (all APIs) and categories.json (sidebar).
    """
    # 1. All APIs
    all_apis = []
    for cat, apis in categorized.items():
        for api in apis:
            all_apis.append(asdict(api))

    apis_path = os.path.join(output_dir, "apis.json")
    with open(apis_path, "w", encoding="utf-8") as f:
        json.dump(all_apis, f, indent=2)

    # 2. Categories for the sidebar
    cats = [{"name": cat, "count": len(apis)} for cat, apis in categorized.items()]
    cats_path = os.path.join(output_dir, "categories.json")
    with open(cats_path, "w", encoding="utf-8") as f:
        json.dump({"categories": cats}, f, indent=2)

    logger.info("Exported apis.json and categories.json for web showcase")
