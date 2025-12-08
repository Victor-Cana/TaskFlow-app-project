import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Create a New Project")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_project_name" not in st.session_state:
    st.session_state.success_project_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(project_name):
    st.markdown(f"### {project_name} has been successfully created!")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to CFO Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_project_name = ""
            st.switch_page("pages/10_Client_CFO_Home.py")
    
    with col2:
        if st.button("Add Another Project", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_project_name = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# API endpoint
API_URL = "http://web-api:4000/client_cfo/projects"

# Create a form for project details with dynamic key to force reset
with st.form(f"create_project_form_{st.session_state.form_key_counter}"):
    st.subheader("Project Information")

    # Required fields marked with *
    manager_id = st.number_input("Manager ID *", min_value=1, step=1)
    creator_id = st.number_input("Creator ID *", min_value=1, step=1)
    
    # Optional fields
    project_name = st.text_input("Project Name")
    description = st.text_area("Description")
    date_due = st.date_input("Due Date", value=None)
    date_managed = st.date_input("Date Managed", value=None)
    date_created = st.date_input("Date Created", value=None)

    # Form submission button
    submitted = st.form_submit_button("Create Project")

    if submitted:
        # Validate required fields
        if not all([manager_id, creator_id]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            project_data = {
                "managerID": manager_id,
                "creatorID": creator_id,
                "projectName": project_name if project_name else None,
                "dateDUE": date_due.isoformat() if date_due else None,
                "description": description if description else None,
                "dateManaged": date_managed.isoformat() if date_managed else None,
                "dateCreated": date_created.isoformat() if date_created else None,
            }

            try:
                # Send POST request to API
                response = requests.post(API_URL, json=project_data)

                # Debug: Show what we got back
                st.write(f"Status Code: {response.status_code}")
                st.write(f"Response Text: {response.text}")

                if response.status_code == 201:
                    # Store project name and show modal
                    st.session_state.show_success_modal = True
                    st.session_state.success_project_name = project_name if project_name else f"Project {project_id}"
                    st.rerun()
                else:
                    try:
                        error_msg = response.json().get('error', 'Unknown error')
                    except:
                        error_msg = response.text
                    st.error(f"Failed to create Project: {error_msg}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if project was created successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_project_name)

# Add a button to return to the CFO Home
if st.button("Return to CFO Home", type="primary"):
    st.switch_page("pages/10_Client_CFO_Home.py")