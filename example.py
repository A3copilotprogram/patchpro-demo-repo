
import os  # unused import (intentional)

# The following line will trigger Semgrep's hardcoded password rule
password = "hardcoded_password123"


def add(a, b):
    return a + b

# Sample function to trigger PatchPro CI feedback
def multiply(a, b):
    result = a * b  # result is assigned but not used (lint error)
    return a * b
