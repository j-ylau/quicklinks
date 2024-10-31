import streamlit as st
from streamlit_option_menu import option_menu
from components.admin import show_admin_dashboard
from components.links import show_links_manager, show_link_creator, show_trees
from database.operations import is_admin
from utils.callbacks import logout_callback

def show_dashboard():
    with st.sidebar:
        st.markdown("# QuickLinks")
        
        # Add admin menu items if user is admin
        if is_admin(st.session_state['username']):
            options = ["My Links", "New Link", "Your Links (stacked)", "Admin Dashboard"]
            icons = ["link", "plus-circle", "diagram-3", "shield"]
        else:
            options = ["My Links", "New Link", "Your Links (stacked)"]
            icons = ["link", "plus-circle", "diagram-3"]
        
        selected = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            menu_icon=None,
            default_index=0,
        )
        
        st.markdown("---")
        st.button("🚪 Logout", on_click=logout_callback, type="secondary")

    if selected == "Admin Dashboard" and is_admin(st.session_state['username']):
        show_admin_dashboard()
    elif selected == "My Links":
        show_links_manager()
    elif selected == "New Link":
        show_link_creator()
    elif selected == "Your Links (stacked)":
        show_trees()