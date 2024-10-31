import streamlit as st
from database.models import init_db
from utils.session import init_session_state
from utils.styles import load_css
from components.auth import show_auth_page
from components.dashboard import show_dashboard

# Set page config
st.set_page_config(
    page_title="LinkHub Creator",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize app
init_session_state()
init_db()
st.markdown(load_css(), unsafe_allow_html=True)

# Main app logic
if not st.session_state['logged_in']:
    show_auth_page()
else:
    show_dashboard()