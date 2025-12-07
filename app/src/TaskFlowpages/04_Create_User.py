import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Create a New User")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_user_name" not in st.session_state:
    st.session_state.success_user_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(user_name):
    st.markdown(f"### {user_name} has been successfully added to the system!")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Software Engineer Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_user_name = ""
            st.switch_page("TaskFlowpages/00_Software_Engineer_Home.py")
    
    with col2:
        if st.button("Add Another User", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_user_name = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# API endpoint
API_URL = "http://web-api:4000/users" '<-- Update this URL to the correct user creation endpoint'

# Create a form for user details with dynamic key to force reset
with st.form(f"create_user_form_{st.session_state.form_key_counter}"):
    st.subheader("User Information")

    # Required fields marked with *
    email1 = st.text_input("Email *")
    email2 = st.text_input("Email #2")
    email3 = st.text_input("Email #3")
    firstName = st.text_input("First Name *")
    lastName = st.text_input("Last Name *")
    managerID = st.number_input("Manager ID #", value=0, step=1)

    if managerID == 0:
        managerID = None

    # Form submission button
    submitted = st.form_submit_button("Create User")

    if submitted:
        # Validate required fields
        if not all([email1, firstName, lastName]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            user_data = {
                "email1": email1,
                "email2": email2 if email2 else None,
                "email3": email3 if email3 else None,
                "firstName": firstName,
                "lastName": lastName,
                "managerID": managerID if managerID else None,
            }

            try:
                # Send POST request to API
                response = requests.post(API_URL, json=user_data)

                if response.status_code == 201:
                    # Store NGO name and show modal
                    st.session_state.show_success_modal = True
                    st.session_state.success_user_name = firstName + " " + lastName
                    st.rerun()
                else:
                    st.error(
                        f"Failed to add User: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if NGO was added successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_user_name)

# Add a button to return to the NGO Directory
if st.button("Return to Sotware Engineer Home", type="primary"):
    st.switch_page("TaskFlowpages/00_Software_Engineer_Home.py")
