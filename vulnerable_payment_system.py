"""
Payment Processing System - DELIBERATELY FLAWED FOR DEMO
This file contains multiple security, performance, and code quality issues
"""

import os
import pickle
import hashlib
import random
import sqlite3
from datetime import datetime


# SECURITY ISSUE #1: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"
SECRET_KEY = "my-secret-key"


class PaymentProcessor:
    def __init__(self):
        # SECURITY ISSUE #2: SQL Injection vulnerability
        self.db_connection = sqlite3.connect("payments.db")
        
    def process_payment(self, user_id, amount, card_number):
        """Process a payment transaction"""
        
        # SECURITY ISSUE #3: Direct SQL query without parameterization
        query = f"INSERT INTO payments (user_id, amount, card_number) VALUES ({user_id}, {amount}, '{card_number}')"
        self.db_connection.execute(query)
        
        # SECURITY ISSUE #4: Storing sensitive data in plain text
        log_file = open("payment_logs.txt", "a")
        log_file.write(f"Payment: {user_id}, {amount}, {card_number}\n")
        log_file.close()
        
        # PERFORMANCE ISSUE #1: Inefficient loop
        total = 0
        for i in range(1, 1000000):
            total = total + i
        
        return True
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        
        # SECURITY ISSUE #5: Weak password hashing
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        # SECURITY ISSUE #6: SQL injection in WHERE clause
        query = f"SELECT * FROM users WHERE username='{username}' AND password_hash='{password_hash}'"
        result = self.db_connection.execute(query)
        
        return result.fetchone() is not None
    
    def load_user_data(self, filename):
        """Load user data from file"""
        
        # SECURITY ISSUE #7: Unsafe deserialization
        with open(filename, 'rb') as f:
            user_data = pickle.load(f)
        
        return user_data
    
    def generate_transaction_id(self):
        """Generate a unique transaction ID"""
        
        # SECURITY ISSUE #8: Weak random number generation for security
        random_num = random.randint(100000, 999999)
        
        # CODE QUALITY ISSUE #1: Old-style string formatting
        transaction_id = "TXN-%s-%s" % (datetime.now().strftime("%Y%m%d"), random_num)
        
        return transaction_id


def calculate_discount(price, discount_percent):
    """Calculate discounted price"""
    
    # CODE QUALITY ISSUE #2: Unnecessary lambda
    discount_calculator = lambda p, d: p - (p * d / 100)
    
    return discount_calculator(price, discount_percent)


def get_payment_status(payment_id):
    """Get status of a payment"""
    
    # CODE QUALITY ISSUE #3: Bare except clause
    try:
        conn = sqlite3.connect("payments.db")
        # SECURITY ISSUE #9: Another SQL injection
        result = conn.execute(f"SELECT status FROM payments WHERE id={payment_id}")
        return result.fetchone()[0]
    except:
        return "UNKNOWN"


# CODE QUALITY ISSUE #4: Unused imports at the top
# CODE QUALITY ISSUE #5: Missing docstring for module-level code

# SECURITY ISSUE #10: Debug mode enabled in production
DEBUG = True

if DEBUG:
    # SECURITY ISSUE #11: Printing sensitive data
    print(f"Database password: {DATABASE_PASSWORD}")
    print(f"API Key: {API_KEY}")


def process_refund(payment_id, amount):
    """Process a refund"""
    
    # PERFORMANCE ISSUE #2: Redundant computation
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    parsed_time = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
    
    # CODE QUALITY ISSUE #6: Multiple statements on one line
    status = "pending"; approved = False; reason = "none"
    
    return status


# CODE QUALITY ISSUE #7: Unused variable
unused_config = {"timeout": 30, "retries": 3}


class CreditCardValidator:
    """Validate credit card information"""
    
    def __init__(self):
        pass
    
    def validate_card(self, card_number, cvv, expiry):
        """Validate a credit card"""
        
        # SECURITY ISSUE #12: Logging sensitive data
        print(f"Validating card: {card_number}, CVV: {cvv}, Expiry: {expiry}")
        
        # CODE QUALITY ISSUE #8: Comparison to True/False
        if len(card_number) == 16 and cvv != None:
            is_valid = True
        else:
            is_valid = False
        
        if is_valid == True:
            return True
        else:
            return False


# SECURITY ISSUE #13: Command injection vulnerability
def run_payment_report(report_type):
    """Generate payment report"""
    command = f"python generate_report.py --type {report_type}"
    os.system(command)
