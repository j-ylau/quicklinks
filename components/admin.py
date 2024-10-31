# components/admin.py

import streamlit as st
from database.operations import get_all_users, delete_user, get_user_stats

def show_admin_dashboard():
    st.markdown("# 👑 Admin Dashboard")
    
    # Show stats at the top
    stats = get_user_stats()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", stats['total_users'])
    with col2:
        st.metric("Total Links", stats['total_links'])
    with col3:
        st.metric("Active Users", stats['active_users'])
    with col4:
        st.metric("Avg Links/User", f"{stats['avg_links_per_user']:.1f}")
    
    st.markdown("---")
    
    # User Management
    st.markdown("## 👥 User Management")
    
    # Search functionality
    search = st.text_input("🔍 Search users", placeholder="Search by username or email...")
    
    users = get_all_users()
    
    if search:
        users = [user for user in users 
                if search.lower() in user[0].lower() 
                or search.lower() in user[1].lower()]
    
    # User list
    for user in users:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="user-container">
                    <h3>{user[0]}</h3>
                    <p>Email: {user[1]}</p>
                    <p>Created: {user[2]}</p>
                    <p>Links: {user[3]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🔎 View Links", key=f"view_{user[0]}"):
                    st.session_state['viewing_user'] = user[0]
                    st.rerun()
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{user[0]}"):
                    if delete_user(user[0]):
                        st.success(f"User {user[0]} deleted successfully!")
                        st.rerun()