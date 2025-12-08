import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Create a New Report")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_report_id" not in st.session_state:
    st.session_state.success_report_id = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(report_id):
    st.markdown(f"### Report #{report_id} has been successfully created!")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Project Manager Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_report_id = ""
            st.switch_page("pages/22_Project_Manager_Home.py")
    
    with col2:
        if st.button("Create Another Report", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_report_id = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# API endpoint
API_URL = "http://web-api:4000/project_manager/reports"

# Create a form for report details with dynamic key to force reset
with st.form(f"create_report_form_{st.session_state.form_key_counter}"):
    st.subheader("Report Information")
    
    # Required fields marked with *
    projectID = st.number_input("Project ID *", min_value=1, step=1)
    type = st.text_input("Report Type *")
    description = st.text_area("Description *")
    dateDue = st.date_input("Due Date *", value=None)
    
    # Submission button
    submitted = st.form_submit_button("Create Report")

    if submitted:
        # Validate required fields
        if not all([projectID, type, description, dateDue]):  
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            report_data = {
                "projectID": projectID,
                "type": type,
                "description": description,
                "dateDue": dateDue.isoformat()
            }
            
            try:
                # Send POST request to API
                response = requests.post(API_URL, json=report_data)
                
                if response.status_code == 201:
                    # Store report ID and show modal
                    report_id = response.json().get("reportID")
                    st.session_state.show_success_modal = True
                    st.session_state.success_report_id = report_id
                    st.rerun()
                else:
                    st.error(
                        f"Failed to create Report: {response.json().get('error', 'Unknown error')}"
                    )
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if report was created successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_report_id)

# Add a button to return to the Project Manager Home
if st.button("Return to Project Manager Home", type="primary"):
    st.session_state.show_success_modal = False
    st.switch_page("pages/22_Project_Manager_Home.py")
