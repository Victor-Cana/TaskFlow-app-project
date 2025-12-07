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
    st.markdown(f"### {resource_name} has been successfully updated in the system!")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Software Engineer Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_resource_name = ""
            st.switch_page("TaskFlowpages/00_Software_Engineer_Home.py")
    
    with col2:
        if st.button("Update Another Resource", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_resource_name = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# API endpoint
API_URL = "http://web-api:4000/software_engineer/resources"

# Create a form for NGO details with dynamic key to force reset
with st.form(f"update_resource_form_{st.session_state.form_key_counter}"):
    st.subheader("Resource Information")

    resourceID = st.number_input("Resource ID *", min_value=1, step=1)

    # Required fields marked with *
    name = st.text_input("Name *")
    type = st.text_input("Type (.docx, .pdf, .xlxs, etc.)*")
    description = st.text_input("Description")
    link = st.text_input("Resource Link *")
    dateDue = st.date_input("Due Date", value=None)

    # Form submission button
    submitted = st.form_submit_button("Update Resource")

    if submitted:
            # Prepare the data for API
            resource_data = {}
            if name:
                resource_data["name"] = name
            if type:
                resource_data["type"] = type
            if description:
                resource_data["description"] = description
            if link:
                resource_data["link"] = link
            if dateDue:
                resource_data["dateDue"] = dateDue.isoformat()

            if not resource_data:
                st.error("Please provide at least one field to update")
            else:
                try:
                    # Send POST request to API
                    response = requests.put(f"{API_URL}/{resourceID}", json=resource_data)

                    if response.status_code == 200:
                        # Store NGO name and show modal
                        st.session_state.show_success_modal = True
                        st.session_state.success_resource_name = f"Resource #{resourceID}"
                        st.rerun()
                    else:
                        st.error(
                            f"Failed to update Resource: {response.json().get('error', 'Unknown error')}"
                        )

                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the API: {str(e)}")
                    st.info("Please ensure the API server is running")

# Show success modal if NGO was added successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_resource_name)

# Add a button to return to the NGO Directory
if st.button("Return to Sotware Engineer Home", type="primary"):
    st.switch_page("TaskFlowpages/00_Software_Engineer_Home.py")
