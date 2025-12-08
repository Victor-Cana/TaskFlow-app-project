import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Create a New Milestone")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_milestone_name" not in st.session_state:
    st.session_state.success_milestone_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(milestone_name):
    st.markdown(f"### {milestone_name} has been successfully added to the system!")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to CFO Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_milestone_name = ""
            st.switch_page("pages/10_Client_CFO_Home.py")
    
    with col2:
        if st.button("Add Another Milestone", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_milestone_name = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# API endpoint
API_URL = "http://web-api:4000/client_cfo/milestones"

# Create a form for milestone details with dynamic key to force reset
with st.form(f"create_milestone_form_{st.session_state.form_key_counter}"):
    st.subheader("Milestone Information")

    # Required fields marked with *
    project_id = st.number_input("Project ID *", min_value=1, step=1)
    milestone_id = st.number_input("Milestone ID *", min_value=1, step=1)
    
    # Optional fields
    name = st.text_input("Name")
    description = st.text_area("Description")
    display_style = st.selectbox("Display Style", ["", "banner", "card", "featured", "hidden"])

    # Form submission button
    submitted = st.form_submit_button("Create Milestone")

    if submitted:
        # Validate required fields
        if not all([project_id, milestone_id]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            milestone_data = {
                "projectID": project_id,
                "milestoneID": milestone_id,
                "name": name if name else None,
                "description": description if description else None,
                "displayStyle": display_style if display_style else None,
            }

            try:
                # Send POST request to API
                response = requests.post(API_URL, json=milestone_data)

                if response.status_code == 201:
                    # Store milestone name and show modal
                    st.session_state.show_success_modal = True
                    st.session_state.success_milestone_name = name if name else f"Milestone {milestone_id}"
                    st.rerun()
                else:
                    st.error(
                        f"Failed to add Milestone: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if milestone was added successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_milestone_name)

# Add a button to return to the CFO Home
if st.button("Return to CFO Home", type="primary"):
    st.switch_page("pages/10_Client_CFO_Home.py")