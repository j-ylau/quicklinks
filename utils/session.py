import streamlit as st

def init_session_state():
    session_vars = {
        'logged_in': False,
        'username': None,
        'editing_link': None,
        'reset_step': 1,
        'login_username': '',
        'login_password': '',
        'new_username': '',
        'new_password': '',
        'new_email': '',
        'reset_email': '',
        'reset_token': '',
        'new_reset_password': '',
        'confirm_reset_password': '',
        'edit_button_text': '',
        'edit_link_content': '',
        'reset_signup_form': False,
        'signup_success': False,  # Add this line
        'active_tab': 0  # Add this line
    }
    
    for var, default_value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = default_value