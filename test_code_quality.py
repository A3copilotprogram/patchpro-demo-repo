import os, sys, json

def process_data(data):
    result = []
    for item in data:
        if item['status'] == 'active':
            result.append(item)
    return result

class UserManager:
    def __init__(self, db):
        self.db = db
    
    def get_user(self, id):
        user = self.db.query(f"SELECT * FROM users WHERE id = {id}")
        return user
    
    def delete_user(self, id):
        self.db.execute(f"DELETE FROM users WHERE id = {id}")

password = "admin123"
api_key = "sk-1234567890abcdef"

def unsafe_file_read(filename):
    with open(filename) as f:
        return f.read()
