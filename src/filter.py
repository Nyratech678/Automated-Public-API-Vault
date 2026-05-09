#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#=========================================================================
# STANDARD LIBRARIES
#=========================================================================

import logging
from datetime import datetime, timedelta, timezone
from src.models import API

logger = logging.getLogger(__name__)

#=========================================================================
# FILTER FUNCTION
#=========================================================================

def filter_inactive(apis: list[API], threshold_months: int = 12) -> tuple[list[API], list[API]]:
    """
Filter out APIs that have not been updated in the last 'threshold_months' months.
    """
    active = []
    inactive = []
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=threshold_months*30)

    for api in apis:
        if api.archived:
            inactive.append(api)
            continue

        if api.updated_at:
            try:
                updated = datetime.fromisoformat(api.updated_at.replace('Z', '+00:00'))
                if updated < cutoff_date:
                    inactive.append(api)
                    continue
            except ValueError:
                logger.warning(f"Invalid date format for API {api.name}: {api.updated_at}")
                inactive.append(api)
                continue
        else:
            inactive.append(api)
            continue

        active.append(api)
    
    logger.info(f"Filtered APIs: {len(active)} active, {len(inactive)} inactive (threshold: {threshold_months} months)")
    return active, inactive