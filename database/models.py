# database/models.py

import sqlite3
from datetime import datetime
import hashlib

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create tables with all columns - remove DROP statements
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT,
                  email TEXT,
                  reset_token TEXT NULL,
                  reset_token_expiry DATETIME NULL,
                  created_at DATETIME,
                  is_admin BOOLEAN DEFAULT 0)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS links
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  button_text TEXT,
                  link_content TEXT,
                  position INTEGER,
                  created_at DATETIME,
                  FOREIGN KEY (username) REFERENCES users(username))''')
    
    # Create admin account if it doesn't exist
    admin_username = "helloworld"
    admin_password = "helloworld"
    admin_email = "helloworld@gmail.com"
    
    c.execute("SELECT username FROM users WHERE username=?", (admin_username,))
    if not c.fetchone():
        hashed_password = hashlib.sha256(str.encode(admin_password)).hexdigest()
        c.execute("""INSERT INTO users 
                    (username, password, email, reset_token, reset_token_expiry, created_at, is_admin)
                    VALUES (?, ?, ?, NULL, NULL, ?, 1)""",
                 (admin_username, hashed_password, admin_email, datetime.now()))
    
    conn.commit()
    conn.close()