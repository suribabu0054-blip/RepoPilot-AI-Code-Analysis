"""
Sample Python Code for Testing RepoPilot
This file contains various code patterns for demonstration
"""

import os
import hashlib
import json


# Example 1: User Authentication (with security issues)
def authenticate_user(username, password):
    """
    Authenticate user with username and password
    WARNING: This code has security vulnerabilities for demonstration
    """
    # Hardcoded credentials (BAD PRACTICE!)
    admin_password = "admin123"
    
    if username == "admin" and password == admin_password:
        return True
    
    # Using MD5 for password hashing (WEAK!)
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    # SQL query with string formatting (SQL INJECTION RISK!)
    query = "SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, hashed)
    
    # Execute query (dangerous!)
    result = os.system(query)
    
    return result


# Example 2: Data Processing (can be modernized)
def process_data(items):
    """Process list of items"""
    result = []
    for item in items:
        result.append(item * 2)
    return result


# Example 3: File Operations (missing context manager)
def read_config(filename):
    """Read configuration from file"""
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return json.loads(data)


# Example 4: String Formatting (old style)
def generate_message(name, age):
    """Generate greeting message"""
    return "Hello %s, you are %d years old" % (name, age)


# Example 5: Class without type hints
class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, username, email):
        user = {"username": username, "email": email}
        self.users.append(user)
        return user
    
    def get_user(self, username):
        for user in self.users:
            if user["username"] == username:
                return user
        return None
    
    def delete_user(self, username):
        self.users = [u for u in self.users if u["username"] != username]


# Example 6: API Key exposure
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"


# Example 7: Unsafe deserialization
def load_data(data):
    """Load serialized data"""
    import pickle
    return pickle.loads(data)


# Example 8: No error handling
def divide_numbers(a, b):
    """Divide two numbers"""
    return a / b


# Example 9: Eval usage (dangerous)
def calculate(expression):
    """Calculate mathematical expression"""
    return eval(expression)


# Main execution
if __name__ == "__main__":
    # Test authentication
    result = authenticate_user("admin", "admin123")
    print("Authentication result:", result)
    
    # Test data processing
    data = [1, 2, 3, 4, 5]
    processed = process_data(data)
    print("Processed data:", processed)
    
    # Test user manager
    manager = UserManager()
    manager.add_user("john", "john@example.com")
    user = manager.get_user("john")
    print("User:", user)

# Made with Bob
