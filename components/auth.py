# components/auth.py

import streamlit as st
from utils.callbacks import login_callback, signup_callback
from database.operations import generate_reset_token, verify_reset_token, reset_password


def show_auth_page():
    # Check if we need to reset the signup form
    if st.session_state.get('reset_signup_form'):
        if 'new_username' in st.session_state:
            del st.session_state['new_username']
        if 'new_password' in st.session_state:
            del st.session_state['new_password']
        if 'new_email' in st.session_state:
            del st.session_state['new_email']
        del st.session_state['reset_signup_form']

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# ✨ Quick Links")
        st.markdown("### Share your links effortlessly")

        # Show signup success message if present
        if st.session_state.get('signup_success'):
            st.success("✨ Account created successfully! Please login with your credentials.")
            del st.session_state['signup_success']
        
        # Initialize tab selection
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 0
            
        tab1, tab2, tab3 = st.tabs(["🔑 Login", "✨ Sign Up", "🔄 Reset Password"])
        
        # Switch to login tab after successful signup
        if st.session_state.active_tab == 0:
            tab1.is_selected = True
            
        with tab1:
            with st.form("login_form"):
                st.text_input("👤 Username", key="login_username")
                st.text_input("🔒 Password", type="password", key="login_password")
                submit = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                if submit:
                    login_callback()
        
        with tab2:
            with st.form("signup_form"):
                st.text_input("👤 Username", key="new_username")
                st.text_input("🔒 Password", type="password", key="new_password")
                st.text_input("📧 Email", key="new_email")
                submit = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
                
                if submit:
                    signup_callback()
        
        with tab3:
            if "reset_step" not in st.session_state:
                st.session_state.reset_step = 1
            
            if st.session_state.reset_step == 1:
                with st.form("reset_request_form"):
                    st.text_input("📧 Email", key="reset_email")
                    submit = st.form_submit_button("Request Reset Link", 
                                                 type="primary", 
                                                 use_container_width=True)
                    
                    if submit:
                        token = generate_reset_token(st.session_state.reset_email)
                        if token:
                            st.success("Reset link sent to your email! (Token: " + token + ")")
                            st.session_state.reset_step = 2
                        else:
                            st.error("Email not found!")
            
            elif st.session_state.reset_step == 2:
                with st.form("reset_password_form"):
                    st.text_input("🔑 Reset Token", key="reset_token")
                    st.text_input("🔒 New Password", type="password", key="new_reset_password")
                    st.text_input("🔒 Confirm Password", type="password", key="confirm_reset_password")
                    submit = st.form_submit_button("Reset Password", 
                                                 type="primary", 
                                                 use_container_width=True)
                    
                    if submit:
                        if st.session_state.new_reset_password != st.session_state.confirm_reset_password:
                            st.error("Passwords don't match!")
                        else:
                            if reset_password(st.session_state.reset_token, 
                                           st.session_state.new_reset_password):
                                st.success("Password reset successfully! Please login.")
                                st.session_state.reset_step = 1
                            else:
                                st.error("Invalid or expired reset token!")

        # Handle callbacks outside forms
        if st.session_state.get('trigger_login'):
            login_callback()
            del st.session_state.trigger_login
            
        if st.session_state.get('trigger_signup'):
            signup_callback()
            del st.session_state.trigger_signup