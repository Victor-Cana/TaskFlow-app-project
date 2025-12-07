import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Update a Resource")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_resource_name" not in st.session_state:
    st.session_state.success_resource_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(resource_name):
    st.markdown(f"### {resource_name} has been successfully deleted!")

    if st.button("OK", use_container_width=True):
        st.rerun()

API_URL = "http://web-api:4000/software_engineer/resources"

# Fetch resources
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    resources = response.json()
except requests.exceptions.RequestException as e:
    st.error("Failed to load resources")
    st.stop()

if not resources:
    st.info("No resources available.")
    st.stop()

# Table header
cols = st.columns([1, 3, 2, 3, 3])
cols[0].write("**ID**")
cols[1].write("**Name**")
cols[2].write("**Type**")
cols[3].write("**Link**")
cols[4].write("")

# Table rows
for resource in resources:
    col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 3, 3])

    col1.write(resource["resourceID"])
    col2.write(resource["name"])
    col3.write(resource["type"])
    col4.write(resource["link"])

    if col5.button("❌ Delete", key=f"delete_{resource['resourceID']}"):
        delete_response = requests.delete(
            f"{API_URL}/{resource['resourceID']}"
        )

        if delete_response.status_code == 200:
            show_success_dialog(resource["name"])
        else:
            st.error(
                delete_response.json().get("error", "Failed to delete resource")
            )

if st.button("Return to Software Engineer Home", type="primary"):
    st.switch_page("TaskFlowpages/00_Software_Engineer_Home.py")
