"""Demo file to show PatchPro local dev workflow."""

import json  # unused
import sys


def calculate_total(items):
    """Calculate total price."""
    total = 0
    for item in items:
        total = total + item['price']
    return total


def validate_user(username, password):
    """Validate user credentials."""
    # Bad: comparison with None using ==
    if username == None:
        return False
    
    # Bad: bare except
    try:
        result = check_database(username, password)
        return result
    except:
        return False


def check_database(username, password):
    """Mock database check."""
    return True
