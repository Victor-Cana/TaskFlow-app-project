import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About TaskFlow")

st.markdown(
    """
    TaskFlow is a demo app for the CS3200: Introduction to Databases 2025 Fall Semester Course Project.

    TaskFlow is a platform that allows users to create, organize, and complete a wide variety of 
    collaborative projects through an intuitive, curated interface for each role within the team.

    This demo app showcases the intended functionality for each role, powered by a self-developed tech stack.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("TaskFlowHome.py")
