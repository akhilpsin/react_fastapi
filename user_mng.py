import json
import hashlib
from pathlib import Path

def read_dictionary_from_file(filepath):
    """
    Reads a dictionary from a JSON file.
    """
    file = Path(filepath)
    if not file.exists():
        print(f"File not found: {filepath}. Creating a new one.")
        return {}
    try:
        with file.open('r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error parsing JSON in {filepath}.")
        return {}

def update_local_file(filepath, log_db_dict):
    """
    Writes the dictionary to a JSON file.
    """
    with open(filepath, "w") as file:
        json.dump(log_db_dict, file, indent=4)

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(log_db, filepath, username, fname, lname, email, ph, psw):
    """
    Registers a new user if the username does not exist.
    """
    if username in log_db:
        return "Username already exists"
    
    log_db[username] = {
        'username': username,
        'email': email,
        'phone': ph,
        'first_name': fname,
        'last_name': lname,
        'hashed_password': hash_password(psw),
        'disabled': False
    }
    update_local_file(filepath, log_db)
    return "User registered successfully"

def login(log_db, username, psw):
    """
    Logs in a user by verifying credentials.
    """
    user = log_db.get(username)
    if not user:
        return "Invalid username"
    if user['hashed_password'] != hash_password(psw):
        return "Incorrect password"
    if user['disabled']:
        return "Account is disabled"
    return "Login successful"

def remove_user(log_db, filepath, username):
    """
    Removes a user if they exist.
    """
    if username not in log_db:
        return "User not found"
    
    del log_db[username]
    update_local_file(filepath, log_db)
    return "User removed successfully"

def toggle_user_status(log_db, filepath, username, disable=True):
    """
    Enables or disables a user account.
    """
    if username not in log_db:
        return "User not found"
    
    log_db[username]['disabled'] = disable
    update_local_file(filepath, log_db)
    return "User {} successfully".format("disabled" if disable else "activated")

# Filepath and database initialization
login_file = 'log_users.json'
log_db = read_dictionary_from_file(login_file)

# Example Usage
if log_db is not None:
    #print(register_user(log_db, login_file, "aps23", "Akhil3", "P S", "akhilpsinbox@gmail.com", "15510248642", "password"))
    #print(log_db)
    print(login(log_db, "ap", "password"))
else:
    print("Failed to read user database.")
