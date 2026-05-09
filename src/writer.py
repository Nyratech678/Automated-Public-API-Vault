#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#=========================================================================
# STANDARD LIBRARIES
#=========================================================================
import os
import json
import shutil
import logging
from jinja2 import Environment, FileSystemLoader
from src.models import API

logger = logging.getLogger(__name__)

#=========================================================================
# UTILITY FUNCTIONS
#=========================================================================

def _write_if_changed(path: str, content: str) -> bool:
    """
    Write 'content' in 'path only if file not exists 
    or if his actual content is different.
    Return true if a write was performed, false otherwise.
    """
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                existing = f.read()
            if existing == content:
                logger.debug(f"No changes for {path}, skipping write.")
                return False
        except OSError:
            pass
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Wrote file: {path}")
        return True
    except OSError as e:
        logger.error(f"Error writing file {path}: {e}")
        return False

#=========================================================================
# WRITE README.md FUNCTION
#=========================================================================

def write_readmes(categorized: dict[str, list[API]],
                  templates_dir: str = "templates",
                  output_base: str = "categories") -> dict[str, int]:
    """
    Write a README.md file for each category using Jinja2 templates.
    Returns a dict mapping category -> number of APIs written.
    """
    env = Environment(loader=FileSystemLoader(templates_dir))

    counts: dict[str, int] = {}

    for cat, apis in categorized.items():
        cat_dir = os.path.join(output_base, cat)
        try:
            os.makedirs(cat_dir, exist_ok=True)
        except OSError as e:
            logger.error(f"Error creating directory {cat_dir}: {e}")
            continue
        
        try:
            template = env.get_template("category_readme.md.j2")
            content = template.render(category_name=cat, apis=apis)
        except Exception as e:
            logger.error(f"Error rendering template for category {cat}: {e}")
            continue

        readme_path = os.path.join(cat_dir, "README.md")
        _write_if_changed(readme_path, content)
        counts[cat] = len(apis)
    
    if os.path.isdir(output_base):
        existing_dirs = [d for d in os.listdir(output_base) if os.path.isdir(os.path.join(output_base, d))]

        for d in existing_dirs:
            if d not in categorized:
                try:
                    shutil.rmtree(os.path.join(output_base, d))
                    logger.info(f"Removed obsolete category directory: {d}")
                except OSError as e:
                    logger.error(f"Error removing directory {d}: {e}")
    try:
        main_template = env.get_template("main_readme.md.j2")
        main_content = main_template.render(categories=list(categorized.keys()))
        _write_if_changed("README.md", main_content)
    except Exception as e:
        logger.error(f"Error writing main README.md: {e}")
        raise

    return counts

#=========================================================================
# EXPORT FOR SITE FUNCTION
#=========================================================================

def export_for_site(categorized: dict[str, list[API]], output_dir: str = ".") -> None:
    """
    Genere apis.json (toutes les APIs) et categories.json (sidebar).
    """
    all_apis = []
    for cat, apis in categorized.items():
        for api in apis:
            all_apis.append({
                "name": api.name,
                "description": api.description,
                "topics": api.topics,
                "language": api.language,
                "license": api.license,
                "stars": api.stars,
                "updated_at": api.updated_at,
                "archived": api.archived,
                "url": api.url,
                "homepage": api.homepage,
            })

    apis_path = os.path.join(output_dir, "apis.json")
    with open(apis_path, "w", encoding="utf-8") as f:
        json.dump(all_apis, f, indent=2)

    cats = [{"name": cat, "count": len(apis)} for cat, apis in categorized.items()]
    cats_path = os.path.join(output_dir, "categories.json")
    with open(cats_path, "w", encoding="utf-8") as f:
        json.dump({"categories": cats}, f, indent=2)

    logger.info("Exported apis.json and categories.json for web vitrine")