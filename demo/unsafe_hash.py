import hashlib, os  # ruff: E401 (multiple imports on one line), F401 (unused 'os')

def bad_digest(data: bytes) -> str:
    m = hashlib.md5(data)  # semgrep: insecure hash (use sha256)
    return m.hexdigest()
