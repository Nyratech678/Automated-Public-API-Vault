#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#=========================================================================
# STANDARD LIBRARY IMPORTS
#=========================================================================
import logging

#=========================================================================
# MAIN FUNCTION
#=========================================================================

def setup_logging():
    """Set up logging basic configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )