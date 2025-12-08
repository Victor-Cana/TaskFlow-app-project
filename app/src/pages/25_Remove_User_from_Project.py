import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Remove User from Project")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_message" not in st.session_state:
    st.session_state.success_message = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(message):
    st.markdown(f"### {message}")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Project Manager Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_message = ""
            st.switch_page("pages/20_Project_Manager_Home.py")
    
    with col2:
        if st.button("Remove Another User", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_message = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# API endpoint
API_URL = "http://web-api:4000/project_manager/assignments"

# Create a form for removing user
with st.form(f"remove_user_form_{st.session_state.form_key_counter}"):
    st.subheader("Remove User Information")
    
    # Required fields marked with *
    projectID = st.number_input("Project ID *", min_value=1, step=1)
    userID = st.number_input("User ID *", min_value=1, step=1)
    
    # Form submission button
    submitted = st.form_submit_button("Remove User")
    
    if submitted:
        # Validate required fields
        if not all([projectID, userID]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            assignment_data = {
                "projectID": projectID,
                "userID": userID
            }
            
            try:
                # Send DELETE request to API
                response = requests.delete(API_URL, json=assignment_data)
                
                if response.status_code == 200:
                    # Show success modal
                    st.session_state.show_success_modal = True
                    st.session_state.success_message = f"User #{userID} removed from Project #{projectID}"
                    st.rerun()
                else:
                    st.error(
                        f"Failed to remove user: {response.json().get('error', 'Unknown error')}"
                    )
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if user was removed successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_message)

# Add a button to return to the Project Manager Home
if st.button("Return to Project Manager Home", type="primary"):
    st.session_state.show_success_modal = False
    st.switch_page("pages/20_Project_Manager_Home.py")