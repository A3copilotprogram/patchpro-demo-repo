"""
User Authentication Module - DELIBERATELY FLAWED FOR DEMO
Contains authentication vulnerabilities and code quality issues
"""

import hashlib
import os
import sys
import json
import re
from datetime import datetime, timedelta


# SECURITY ISSUE #1: Hardcoded JWT secret
JWT_SECRET = "super-secret-key-12345"

# SECURITY ISSUE #2: Weak default password
DEFAULT_PASSWORD = "password123"


class UserAuthenticator:
    """Handle user authentication"""
    
    def __init__(self):
        self.users = {}
        self.sessions = {}
    
    def create_user(self, username, password, email):
        """Create a new user account"""
        
        # SECURITY ISSUE #3: No password strength validation
        # CODE QUALITY ISSUE #1: Unnecessary escape in regex
        if not re.match(r"^[\w\.\-]+@[\w\.\-]+\.\w+$", email):
            return False
        
        # SECURITY ISSUE #4: Weak hashing algorithm
        password_hash = hashlib.sha1(password.encode()).hexdigest()
        
        # CODE QUALITY ISSUE #2: Mutable default argument
        user_data = self.initialize_user_data()
        user_data['username'] = username
        user_data['password_hash'] = password_hash
        user_data['email'] = email
        
        self.users[username] = user_data
        
        # SECURITY ISSUE #5: Storing password in logs
        self.log_action(f"User created: {username} with password {password}")
        
        return True
    
    def initialize_user_data(self, roles=[]):
        """Initialize user data structure"""
        # CODE QUALITY ISSUE #3: Mutable default argument
        return {
            'created_at': datetime.now(),
            'roles': roles,
            'failed_attempts': 0
        }
    
    def login(self, username, password):
        """Authenticate a user"""
        
        # CODE QUALITY ISSUE #4: Bare except
        try:
            user = self.users[username]
        except:
            return None
        
        # SECURITY ISSUE #6: Weak password hashing
        password_hash = hashlib.sha1(password.encode()).hexdigest()
        
        # SECURITY ISSUE #7: No rate limiting on login attempts
        if user['password_hash'] == password_hash:
            # SECURITY ISSUE #8: Predictable session tokens
            session_token = f"{username}_{datetime.now().timestamp()}"
            self.sessions[session_token] = username
            
            # SECURITY ISSUE #9: Logging successful login with password
            print(f"Login successful: {username} with password {password}")
            
            return session_token
        else:
            # SECURITY ISSUE #10: No account lockout after failed attempts
            user['failed_attempts'] += 1
            return None
    
    def log_action(self, message):
        """Log user actions"""
        # CODE QUALITY ISSUE #5: File not properly closed
        f = open("auth.log", "a")
        f.write(f"{datetime.now()}: {message}\n")
        # Missing f.close()
    
    def check_permission(self, session_token, required_role):
        """Check if user has required permission"""
        
        # CODE QUALITY ISSUE #6: Using type() for comparison
        if type(session_token) != str:
            return False
        
        if session_token not in self.sessions:
            return False
        
        username = self.sessions[session_token]
        user = self.users.get(username)
        
        # CODE QUALITY ISSUE #7: Comparison with True
        if user == None:
            return False
        
        # CODE QUALITY ISSUE #8: Using 'in' for multiple checks inefficiently
        if required_role in user['roles']:
            return True
        return False


def reset_password(username, new_password):
    """Reset user password"""
    
    # SECURITY ISSUE #11: No email verification
    # SECURITY ISSUE #12: Weak password hashing
    new_hash = hashlib.md5(new_password.encode()).hexdigest()
    
    # CODE QUALITY ISSUE #9: Using exec (dangerous)
    # exec(f"user_passwords['{username}'] = '{new_hash}'")
    
    # CODE QUALITY ISSUE #10: Print instead of proper logging
    print(f"Password reset for {username} to {new_password}")
    
    return True


def validate_email(email):
    """Validate email format"""
    
    # CODE QUALITY ISSUE #11: Unnecessary else after return
    if "@" in email and "." in email:
        return True
    else:
        return False


def generate_api_key(user_id):
    """Generate API key for user"""
    
    # SECURITY ISSUE #13: Weak random key generation
    import random
    random.seed(user_id)  # Predictable seed!
    
    key_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    api_key = ""
    
    # PERFORMANCE ISSUE #1: Inefficient string concatenation
    for i in range(32):
        api_key = api_key + random.choice(key_chars)
    
    return api_key


def check_password_strength(password):
    """Check if password meets security requirements"""
    
    # CODE QUALITY ISSUE #12: Redundant boolean comparison
    has_upper = False
    has_lower = False
    has_digit = False
    
    for char in password:
        if char.isupper() == True:
            has_upper = True
        if char.islower() == True:
            has_lower = True
        if char.isdigit() == True:
            has_digit = True
    
    # CODE QUALITY ISSUE #13: Can be simplified
    if has_upper and has_lower and has_digit and len(password) >= 8:
        return True
    else:
        return False


# CODE QUALITY ISSUE #14: Unused imports
# sys, json are imported but not used


# SECURITY ISSUE #14: Debug credentials in code
TEST_USERS = {
    "admin": "admin123",
    "test": "test123",
    "root": "root123"
}
