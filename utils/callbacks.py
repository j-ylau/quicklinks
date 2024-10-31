# utils/callbacks.py

import streamlit as st
from database.operations import login, signup

def login_callback():
    if login(st.session_state['login_username'], st.session_state['login_password']):
        st.session_state['logged_in'] = True
        st.session_state['username'] = st.session_state['login_username']
        st.success("Successfully logged in! 🎉")
        st.rerun()  # Keep this rerun as it's not in a form callback
    else:
        st.error("Invalid username or password ❌")

def logout_callback():
    # Clear all relevant session state
    keys_to_clear = [
        'logged_in', 
        'username', 
        'editing_link',
        'login_username',
        'login_password'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
            
    st.success("Logged out successfully! 👋")

def signup_callback():
    if signup(st.session_state['new_username'], 
             st.session_state['new_password'], 
             st.session_state['new_email']):
        # Store success message in session state
        st.session_state['signup_success'] = True
        # Set a flag to reset form
        st.session_state['reset_signup_form'] = True
        st.rerun()
    else:
        st.error("Username already exists ❌")