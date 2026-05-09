#!/usr/bin/env python3
#-*- coding: utf-8 -*-


#=========================================================================
# STANDARD LIBRARIES
#=========================================================================
import json
import re
import logging
from src.models import API

logger = logging.getLogger(__name__)

#=========================================================================
# LOAD_MAPPING FUNCTION
#=========================================================================

def load_mapping(filepath: str = "category_mapping.json") -> dict[str, list[str]]:
    """
    Load the categorizer mapping -> list of keywords via a JSON file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        logger.info(f"Loaded mapping with {len(mapping)} categories.")
        return mapping
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading mapping: {e}")
        raise

#=========================================================================
# CATEGORIZE FUNCTION
#=========================================================================

def categorize(apis: list[API], mapping: dict[str, list[str]]) -> dict[str, list[API]]:
    """
    Classify a list of APIs into categories according to the hybrid mapping.
    """
    # Regex precompilation
    patterns = {}
    for cat, keywords in mapping.items():
        escaped = '|'.join(re.escape(k) for k in keywords)
        patterns[cat] = re.compile(rf'\b(?:{escaped})\b', re.IGNORECASE)

    categorized: dict[str, list[API]] = {}
    for api in apis:
        matched_cat = None

        # Priority 1: topics
        topics_lower = [t.lower() for t in api.topics]
        for cat in mapping.keys():
            if any(k in topics_lower for k in mapping[cat]):
                matched_cat = cat
                break
        
        # Priority 2: regex on name + description
        if not matched_cat:
            text = f"{api.name} {api.description}"
            for cat, regex in patterns.items():
                if regex.search(text):
                    matched_cat = cat
                    break
        
        # Priority 3: fallback to other
        if not matched_cat:
            matched_cat = "other"

        if matched_cat not in categorized:
            categorized[matched_cat] = []
        categorized[matched_cat].append(api)

        logger.debug(f"{api.name} -> {matched_cat}")

    logger.info(f"Categorization complete. Categories: {list(categorized.keys())}")
    return categorized