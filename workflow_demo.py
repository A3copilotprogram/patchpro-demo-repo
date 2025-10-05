"""Demo: Local developer workflow with PatchPro."""

import json  # This import is unused
import os


def process_items(items):
    """Process a list of items."""
    total = 0
    for item in items:
        # Bad: using + instead of += 
        total = total + item
    return total


def check_user(username):
    """Check if username is valid."""
    # Bad: using == None instead of is None
    if username == None:
        return False
    return True


def handle_error():
    """Handle errors."""
    # Bad: bare except clause
    try:
        result = do_something()
        return result
    except:
        return None


def do_something():
    """Mock function."""
    return 42
