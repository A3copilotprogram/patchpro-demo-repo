"""
Payment processing module with security vulnerabilities.
Demonstrates financial data handling security issues.
"""

import json
import requests

class PaymentProcessor:
    def __init__(self):
        # SECURITY ISSUE: Hardcoded API keys
        self.stripe_key = "sk_live_abcd1234567890"
        self.paypal_secret = "paypal_secret_key_12345"
        
    def process_payment(self, card_number, amount, user_data):
        """Process payment - MULTIPLE SECURITY ISSUES"""
        
        # SECURITY ISSUE: Logging sensitive data
        print(f"Processing payment: Card {card_number}, Amount ${amount}")
        
        # SECURITY ISSUE: Storing PII in plaintext
        customer_data = {
            "card_number": card_number,
            "ssn": user_data.get("ssn"),
            "full_name": user_data.get("name"),
            "address": user_data.get("address")
        }
        
        # SECURITY ISSUE: Writing sensitive data to file
        with open("payments.log", "a") as f:
            f.write(f"{json.dumps(customer_data)}\n")
        
        # SECURITY ISSUE: Insecure HTTP for financial API
        api_url = f"http://payment-api.company.com/charge"
        
        # SECURITY ISSUE: No SSL verification
        response = requests.post(
            api_url, 
            json=customer_data,
            verify=False  # Disables SSL verification
        )
        
        return response.json()
    
    def validate_card(self, card_number):
        """Validate credit card - WEAK VALIDATION"""
        # SECURITY ISSUE: No proper card validation
        return len(card_number) == 16
    
    def calculate_fees(self, amount):
        """Calculate fees - POTENTIAL OVERFLOW"""
        # SECURITY ISSUE: No bounds checking
        fee_rate = 0.029
        return amount * fee_rate * 1000000  # Could cause overflow

# SECURITY ISSUE: Global variables with sensitive data
MASTER_ENCRYPTION_KEY = "1234567890abcdef"
ADMIN_OVERRIDE_PASSWORD = "backdoor123"