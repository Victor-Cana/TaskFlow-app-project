import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Update a Message")

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
            st.switch_page("pages/22_Project_Manager_Home.py")
    
    with col2:
        if st.button("Update Another Message", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_message = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# Create a form for updating message
with st.form(f"update_message_form_{st.session_state.form_key_counter}"):
    st.subheader("Update Message Information")
    
    # Required fields marked with *
    messageID = st.number_input("Message ID *", min_value=1, step=1)
    messageBody = st.text_area("New Message Body *", height=150)
    
    # Form submission button
    submitted = st.form_submit_button("Update Message")
    
    if submitted:
        # Validate required fields
        if not all([messageID, messageBody]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            message_data = {
                "messageBody": messageBody
            }
            
            try:
                # Send PUT request to API
                API_URL = f"http://web-api:4000/project_manager/messages/{messageID}"
                response = requests.put(API_URL, json=message_data)
                
                if response.status_code == 200:
                    # Show success modal
                    st.session_state.show_success_modal = True
                    st.session_state.success_message = f"Message #{messageID} updated successfully!"
                    st.rerun()
                else:
                    st.error(
                        f"Failed to update message: {response.json().get('error', 'Unknown error')}"
                    )
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if message was updated successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_message)

# Add a button to return to the Project Manager Home
if st.button("Return to Project Manager Home", type="primary"):
    st.switch_page("pages/22_Project_Manager_Home.py")