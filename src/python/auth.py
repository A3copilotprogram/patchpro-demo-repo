"""
Authentication module with deliberate security vulnerabilities.
This file contains various security issues that PatchPro should detect.
"""

import hashlib
import sqlite3
import secrets

# SECURITY ISSUE: Hardcoded database credentials
DB_PASSWORD = "admin123"
DB_HOST = "prod-db.company.com"

class AuthManager:
    def __init__(self):
        # SECURITY ISSUE: Hardcoded secret key
        self.secret_key = "my-super-secret-key-2024"
        self.db_path = "users.db"
        
    def authenticate_user(self, username, password):
        """Authenticate user - VULNERABLE TO SQL INJECTION"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        
        conn.close()
        return result is not None
    
    def hash_password(self, password):
        """Hash password - WEAK HASHING"""
        # SECURITY ISSUE: Using MD5 (cryptographically broken)
        return hashlib.md5(password.encode()).hexdigest()
    
    def generate_session_token(self):
        """Generate session token - PREDICTABLE"""
        # SECURITY ISSUE: Predictable token generation
        import time
        return f"session_{int(time.time())}"
    
    def reset_password(self, email):
        """Password reset - INSECURE"""
        # SECURITY ISSUE: Weak random token
        reset_token = str(hash(email))
        return reset_token

# SECURITY ISSUE: Debug mode enabled in production
DEBUG = True
if DEBUG:
    print(f"Database password: {DB_PASSWORD}")
    print(f"Secret key: {AuthManager().secret_key}")# Test comment to trigger workflow
