/**
 * Sample JavaScript Code for Testing RepoPilot
 * This file contains various code patterns for demonstration
 */

// Example 1: User Authentication (with security issues)
function authenticateUser(username, password) {
    // Hardcoded credentials (BAD PRACTICE!)
    const adminPassword = "admin123";
    
    if (username === "admin" && password === adminPassword) {
        return true;
    }
    
    // SQL query with string concatenation (SQL INJECTION RISK!)
    const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;
    
    // Execute query (dangerous!)
    return executeQuery(query);
}

// Example 2: Data Processing (can be modernized)
function processData(items) {
    var result = [];
    for (var i = 0; i < items.length; i++) {
        result.push(items[i] * 2);
    }
    return result;
}

// Example 3: Callback Hell (needs async/await)
function fetchUserData(userId, callback) {
    getUserById(userId, function(user) {
        getOrders(user.id, function(orders) {
            getOrderDetails(orders[0].id, function(details) {
                callback(details);
            });
        });
    });
}

// Example 4: No error handling
function divideNumbers(a, b) {
    return a / b;
}

// Example 5: API Key exposure
const API_KEY = "sk-1234567890abcdef";
const DATABASE_URL = "mongodb://user:password@localhost/db";

// Example 6: Eval usage (dangerous)
function calculate(expression) {
    return eval(expression);
}

// Example 7: Old-style class
function UserManager() {
    this.users = [];
}

UserManager.prototype.addUser = function(username, email) {
    var user = { username: username, email: email };
    this.users.push(user);
    return user;
};

UserManager.prototype.getUser = function(username) {
    for (var i = 0; i < this.users.length; i++) {
        if (this.users[i].username === username) {
            return this.users[i];
        }
    }
    return null;
};

// Example 8: XSS vulnerability
function displayMessage(message) {
    document.getElementById('output').innerHTML = message;
}

// Example 9: Insecure random
function generateToken() {
    return Math.random().toString(36).substring(7);
}

// Example 10: No input validation
function processUserInput(input) {
    const data = JSON.parse(input);
    return data;
}

// Main execution
if (typeof window === 'undefined') {
    // Node.js environment
    const result = authenticateUser("admin", "admin123");
    console.log("Authentication result:", result);
    
    const data = [1, 2, 3, 4, 5];
    const processed = processData(data);
    console.log("Processed data:", processed);
    
    const manager = new UserManager();
    manager.addUser("john", "john@example.com");
    const user = manager.getUser("john");
    console.log("User:", user);
}

// Made with Bob
