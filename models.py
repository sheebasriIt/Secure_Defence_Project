# In-memory user database
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'sheeba': {'password': '12345', 'role': 'uploader'}
}

def add_user(username, password, role):
    users[username] = {'password': password, 'role': role}

def get_user(username):
    return users.get(username)