#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#=========================================================================
# STANDARD LIBRARIES
#=========================================================================

import sys
import argparse
import logging
from src.utils import setup_logging
from src.discover import fetch_apis
from src.categorizer import load_mapping, categorize
from src.writer import write_readmes, export_for_site
from src.filter import filter_inactive

#=========================================================================
# MAIN FUNCTION
#=========================================================================

def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Automated Public API Vault")
    parser.add_argument('--query', type=str, default='topic:api', help='GitHub search query')
    parser.add_argument('--max-results', type=int, default=100, help='Maximum results to fetch')
    args = parser.parse_args()

    logger.info(f"Curation cycle started with query='{args.query}', max_results={args.max_results}")

    # 1. Discovery
    try:
        apis = fetch_apis(query=args.query, max_results=args.max_results)
    except Exception as e:
        logger.error(f"Discovery failed: {e}", exc_info=True)
        return 2
    
    active_apis, inactive_apis = filter_inactive(apis)
    logger.info(f"Active APIs: {len(active_apis)}, Inactive: {len(inactive_apis)}")

    if not active_apis and not inactive_apis:
        logger.warning("No APIs at all. Exiting.")
        return 0

    try:
        mapping = load_mapping()
    except Exception as e:
        logger.error(f"Mapping load failed: {e}", exc_info=True)
        return 2

    try:
        categorized = categorize(active_apis, mapping)
    except Exception as e:
        logger.error(f"Categorization failed: {e}", exc_info=True)
        return 2

    if inactive_apis:
        categorized['inactive'] = inactive_apis

    if not categorized:
        logger.warning("No categories generated. Exiting.")
        return 0

    # 4. Write
    try:
        counts = write_readmes(categorized)
        export_for_site(categorized)
    except Exception as e:
        logger.error(f"Write failed: {e}", exc_info=True)
        return 2

    summary_parts = ', '.join(f"{cat}: {count}" for cat, count in counts.items())
    summary_line = f"SUMMARY:{summary_parts}"
    print(summary_line)
    logger.info(f"Change summary: {summary_parts}")

    logger.info("Curation cycle completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())