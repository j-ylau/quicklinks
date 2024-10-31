import streamlit as st
import time
import pyperclip
from database.operations import get_user_links, save_link, update_link, delete_link

def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        st.toast(f"Copied to clipboard! ✨")
    except Exception as e:
        st.error(f"Could not copy to clipboard: {e}")

def show_links_manager():
    st.markdown("# 🔗 My Links")
    links = get_user_links(st.session_state['username'])
    
    if not links:
        st.info("🌱 Start by creating your first link!")
        if st.button("➕ Create Your First Link"):
            st.session_state["navigation_selection"] = "New Link"
            st.rerun()
        return
    
    if not links:
        st.info("🌱 Start by creating your first link!")
        if st.button("➕ Create Your First Link"):
            st.session_state['selected'] = "New Link"
            st.rerun()
        return

    # Search functionality
    search = st.text_input("🔍 Search your links", placeholder="Type to search...")
    filtered_links = links
    if search:
        filtered_links = [link for link in links 
                         if search.lower() in link[1].lower() 
                         or search.lower() in link[2].lower()]
        
    for link in filtered_links:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="link-container">
                    <h3>{link[1]}</h3>
                    <p>{link[2][:50] + '...' if len(link[2]) > 50 else link[2]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✏️", key=f"edit_{link[0]}", help="Edit this link"):
                    st.session_state['editing_link'] = link[0]
                    st.session_state['edit_button_text'] = link[1]
                    st.session_state['edit_link_content'] = link[2]
                    st.rerun()
            
            with col3:
                if st.button("🗑️", key=f"delete_{link[0]}", help="Delete this link"):
                    if delete_link(link[0]):
                        st.toast("Link deleted successfully! 🗑️")
                        time.sleep(0.5)
                        st.rerun()
        
        if st.session_state.get('editing_link') == link[0]:
            with st.form(key=f"edit_form_{link[0]}"):
                new_button_text = st.text_input("Button Text", 
                                              value=st.session_state['edit_button_text'])
                new_link_content = st.text_input("Link Content", 
                                               value=st.session_state['edit_link_content'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Save Changes"):
                        if update_link(link[0], new_button_text, new_link_content):
                            st.success("Link updated successfully! ✨")
                            st.session_state['editing_link'] = None
                            st.rerun()
                with col2:
                    if st.form_submit_button("❌ Cancel"):
                        st.session_state['editing_link'] = None
                        st.rerun()

def show_link_creator():
    st.markdown("# ➕ Create New Link")
    
    links_count = len(get_user_links(st.session_state['username']))
    if links_count >= 10:
        st.error("⚠️ You've reached the maximum limit of 10 links!")
        st.info("💡 Try editing or deleting existing links to make space for new ones.")
        return
    
    with st.form(key="create_link", clear_on_submit=True):
        st.markdown("### Link Details")
        button_text = st.text_input("🏷️ Button Label", 
                                  placeholder="Enter a catchy button label...",
                                  help="This is what people will see on your button")
        
        link_type = st.selectbox("📎 Content Type", 
                               ["URL", "Text", "Email", "Phone"],
                               help="Choose what type of content this button will copy")
        
        if link_type == "URL":
            link_content = st.text_input("🔗 URL", 
                                       placeholder="https://...",
                                       help="Enter the full URL including https://")
        elif link_type == "Text":
            link_content = st.text_area("📝 Text", 
                                      placeholder="Enter the text you want to share...",
                                      help="This text will be copied when someone clicks the button")
        elif link_type == "Email":
            link_content = st.text_input("📧 Email Address",
                                       placeholder="example@email.com",
                                       help="Enter your email address")
        else:
            link_content = st.text_input("📞 Phone Number",
                                       placeholder="+1234567890",
                                       help="Enter your phone number with country code")

        submitted = st.form_submit_button("💾 Save Link", 
                                       use_container_width=True,
                                       type="primary")
        
        if submitted:
            if not button_text or not link_content:
                st.warning("⚠️ Please fill in all fields!")
                return
            
            if link_type == "URL" and not link_content.startswith(("http://", "https://")):
                link_content = "https://" + link_content
            
            if save_link(st.session_state['username'], button_text, link_content, links_count + 1):
                st.balloons()
                st.success("🎉 Link created successfully!")
                time.sleep(1)
                st.rerun()

# Preview now outside the form
    if button_text and link_content:
        st.markdown("### Preview")
        if st.button(button_text, use_container_width=True, key="preview_button"):
            copy_to_clipboard(link_content)

def show_trees():
    st.markdown("# 🎯 My Links")
    
    links = get_user_links(st.session_state['username'])
    if not links:
        st.info("👋 Create some links first to build your tree!")
        if st.button("➕ Create Your First Link"):
            st.session_state['selected'] = "New Link"
            st.rerun()
        return

    # st.markdown("### 🎯 Your Links")
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            for link in links:
                if st.button(f"🔗 {link[1]}", 
                           key=f"tree_{link[0]}", 
                           use_container_width=True):
                    copy_to_clipboard(link[2])