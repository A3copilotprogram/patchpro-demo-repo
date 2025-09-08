import os
import sys
import hashlib  # unused import

def insecure_password_storage(password):
    # Insecure: storing password in plain text
    with open("passwords.txt", "a") as f:
        f.write(password + "\n")

def calculate_sum(a, b):
    result = a + b
    unused_variable = 42
    return result

def main():
    print("Starting program...")
    password = input("Enter your password: ")
    insecure_password_storage(password)
    sum_result = calculate_sum(5, 7)
    print("Sum is",sum_result) # bad spacing
    print("Program finished.")

main()
