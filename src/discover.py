#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#=========================================================================
# STANDARD LIBRARIES
#=========================================================================

import os
import time
import logging
import requests
from src.models import API

logger = logging.getLogger(__name__)

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
MAX_PER_PAGE = 100
MAX_TOTAL_RESULTS = 1000

#=========================================================================
# REQUESTS MAKER FUNCTION
#=========================================================================

def _make_request_with_retry(url, params, headers, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp
            elif resp.status_code in (403, 429):
                wait = int(resp.headers.get("Retry-After", 60))
                logger.warning(f"Rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            elif resp.status_code >= 500:
                logger.warning(f"Server error {resp.status_code}, attempt {attempt}")
            else:
                logger.error(f"Unrecoverable error {resp.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed (attempt {attempt}): {e}")
        if attempt < max_retries:
            sleep_time = 2 ** (attempt - 1)
            logger.info(f"Retrying in {sleep_time}s...")
            time.sleep(sleep_time)
    logger.error("Max retries exceeded")
    return None

#=========================================================================
# FETCH_APIS FUNCTION
#=========================================================================

def fetch_apis(query: str = "topic:api", max_results: int = 100) -> list[API]:
    max_results = min(max_results, MAX_TOTAL_RESULTS)
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    all_items: list[API] = []
    page = 1
    while len(all_items) < max_results:
        params = {
            "q": query,
            "per_page": MAX_PER_PAGE,
            "page": page,
            "sort": "stars",
            "order": "desc"
        }
        resp = _make_request_with_retry(GITHUB_SEARCH_URL, params, headers)
        if resp is None:
            break
        data = resp.json()
        items = data.get("items", [])
        if not items:
            break
        for repo in items:
            api = API(
                name=repo["full_name"],
                description=(repo.get("description") or ""),
                topics=repo.get("topics", []),
                url=repo["html_url"],
                stars=repo.get("stargazers_count", 0),
                language=repo.get("language"),
                license=repo.get("license", {}).get("spdx_id") if repo.get("license") else None,
                updated_at=repo.get("updated_at"),
                archived=repo.get("archived", False),
                homepage=repo.get("homepage")
            )
            all_items.append(api)
            if len(all_items) >= max_results:
                break
        logger.info(f"Page {page}: {len(items)} items, total collected: {len(all_items)}")
        page += 1
        if 'rel="next"' not in resp.headers.get("Link", ""):
            break
    logger.info(f"Fetched {len(all_items)} APIs in total")
    return all_items