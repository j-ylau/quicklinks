import sqlite3
import hashlib
from datetime import datetime, timedelta
import secrets
import streamlit as st

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def signup(username, password, email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        hashed_password = hash_password(password)
        c.execute("""INSERT INTO users 
                    (username, password, email, reset_token, reset_token_expiry, created_at, is_admin)
                    VALUES (?, ?, ?, NULL, NULL, ?, 0)""", 
                 (username, hashed_password, email, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        # Debug: Print out the user's details
        hashed_password = hash_password(password)
        c.execute("SELECT * FROM users WHERE username=? AND password=?", 
                 (username, hashed_password))
        user = c.fetchone()
        return user is not None
    finally:
        conn.close()


def save_link(username, button_text, link_content, position):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO links (username, button_text, link_content, position, created_at) 
                    VALUES (?, ?, ?, ?, ?)""", 
                 (username, button_text, link_content, position, datetime.now()))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error saving link: {e}")
        return False
    finally:
        conn.close()

def get_user_links(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    links = c.execute("""SELECT id, button_text, link_content, position 
                        FROM links WHERE username=? 
                        ORDER BY position""", (username,)).fetchall()
    conn.close()
    return links

def update_link(link_id, button_text, link_content):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE links SET button_text=?, link_content=? WHERE id=?", 
                 (button_text, link_content, link_id))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error updating link: {e}")
        return False
    finally:
        conn.close()

def delete_link(link_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM links WHERE id=?", (link_id,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error deleting link: {e}")
        return False
    finally:
        conn.close()

def generate_reset_token(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Check if email exists
    c.execute("SELECT username FROM users WHERE email=?", (email,))
    user = c.fetchone()
    
    if not user:
        return False
    
    # Generate token and set expiry (24 hours from now)
    token = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(hours=24)
    
    c.execute("""UPDATE users 
                 SET reset_token=?, reset_token_expiry=? 
                 WHERE email=?""", 
              (token, expiry, email))
    conn.commit()
    conn.close()
    
    return token

def verify_reset_token(token):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("""SELECT username FROM users 
                 WHERE reset_token=? 
                 AND reset_token_expiry > ?""", 
              (token, datetime.now()))
    
    user = c.fetchone()
    conn.close()
    
    return user[0] if user else None

def reset_password(token, new_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        hashed_password = hash_password(new_password)
        c.execute("""UPDATE users 
                    SET password=?, reset_token=NULL, reset_token_expiry=NULL 
                    WHERE reset_token=?""", 
                 (hashed_password, token))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error resetting password: {e}")
        return False
    finally:
        conn.close()

def is_admin(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else False

def get_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""SELECT username, email, created_at, 
                 (SELECT COUNT(*) FROM links WHERE links.username = users.username) as link_count 
                 FROM users WHERE is_admin = 0""")
    users = c.fetchall()
    conn.close()
    return users

def delete_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        # First delete all user's links
        c.execute("DELETE FROM links WHERE username=?", (username,))
        # Then delete the user
        c.execute("DELETE FROM users WHERE username=? AND is_admin = 0", (username,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error deleting user: {e}")
        return False
    finally:
        conn.close()

def get_user_stats():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    stats = {
        'total_users': 0,
        'total_links': 0,
        'active_users': 0,  # Users with at least one link
        'avg_links_per_user': 0
    }
    
    c.execute("SELECT COUNT(*) FROM users WHERE is_admin = 0")
    stats['total_users'] = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM links")
    stats['total_links'] = c.fetchone()[0]
    
    c.execute("""SELECT COUNT(DISTINCT username) FROM links""")
    stats['active_users'] = c.fetchone()[0]
    
    if stats['total_users'] > 0:
        stats['avg_links_per_user'] = stats['total_links'] / stats['total_users']
    
    conn.close()
    return stats
