# BEGIN CONFLICT: Duplicate add function with different logic
def add(a, b):
    # Conflicting implementation
    return a - b  # Intentional error for conflict
# END CONFLICT

# BEGIN FLAW: Unused variable and insecure code
def insecure_function():
    token = "super_secret_token"
    print("This is insecure!")
# END FLAW

import os  # unused import (intentional)

# The following line will trigger Semgrep's hardcoded password rule
password = "hardcoded_password123"

# Another intentional issue for CI: unused function and hardcoded secret
def unused_function():
    secret = "another_hardcoded_secret"
    pass


def add(a, b):
    return a + b

# Sample function to trigger PatchPro CI feedback
def multiply(a, b):
    result = a * b  # result is assigned but not used (lint error)
    return a * b

# New function with trailing whitespace and style issues  
def divide(a,b):   
    """Division function with style problems."""
    if b==0:
        return None
    return a/b
        
def process_file(filename):
    # Missing file context manager (should use 'with open')
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content
