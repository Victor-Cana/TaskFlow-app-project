import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("See Deadlines")








# Show success modal if get deadlines was successful
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_user_name)

# Add a button to return to the Team Member Home
if st.button("Return to Team Member Home", type="primary"):
    st.switch_page("pages/30_Team_Member_Home.py")