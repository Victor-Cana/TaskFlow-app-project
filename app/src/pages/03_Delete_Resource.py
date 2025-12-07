import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Manage Resources")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_resource_name" not in st.session_state:
    st.session_state.success_resource_name = ""
if "reset_page" not in st.session_state:
    st.session_state.reset_page = False

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(resource_name):
    st.markdown(f"### {resource_name} has been successfully deleted!")
    if st.button("OK", use_container_width=True):
        st.session_state.show_success_modal = False
        st.session_state.success_resource_name = ""
        st.session_state.reset_page = True
        st.rerun()

# API endpoint
API_URL = "http://web-api:4000/software_engineer/resources"

# Retreive resources from backend
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    resources = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Failed to load resources: {e}")
    st.stop()

if not resources:
    st.info("No resources available.")
    st.stop()

# Table header
cols = st.columns([1, 3, 2, 3, 1])
cols[0].write("**ID**")
cols[1].write("**Name**")
cols[2].write("**Type**")
cols[3].write("**Link**")
cols[4].write("**Action**")

# Table rows with delete buttons
for resource in resources:
    col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 3, 1])

    col1.write(resource["resourceID"])
    col2.write(resource["name"])
    col3.write(resource["type"])
    col4.write(resource["link"])

    # Delete button
    if col5.button("❌ Delete", key=f"delete_{resource['resourceID']}"):
        try:
            delete_response = requests.delete(f"{API_URL}/{resource['resourceID']}")
            if delete_response.status_code == 200:
                st.session_state.show_success_modal = True
                st.session_state.success_resource_name = resource["name"]
                st.rerun()
            else:
                st.error(delete_response.json().get("error", "Failed to delete resource"))
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {e}")

# Show modal if a resource was deleted
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_resource_name)

# Return button
if st.button("Return to Software Engineer Home", type="primary"):
    st.switch_page("pages/00_Software_Engineer_Home.py")
