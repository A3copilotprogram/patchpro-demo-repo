"""Quick test file with a few simple issues."""

import os
import sys

# Issue: unused import
import json


def process_data(data):
    """Process some data."""
    # Issue: bare except
    try:
        result = data * 2
        return result
    except:
        return None


# Issue: == comparison with None
def check_value(val):
    if val == None:
        return False
    return True
