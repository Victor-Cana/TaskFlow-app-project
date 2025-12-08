import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Send Project Message")

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
        if st.button("Send Another Message", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_message = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# Create a form for sending message
with st.form(f"send_message_form_{st.session_state.form_key_counter}"):
    st.subheader("Message Information")
    
    # Required fields marked with *
    projectID = st.number_input("Project ID *", min_value=1, step=1)
    messageType = st.selectbox(
        "Message Type *",
        options=["announcement", "update", "reminder", "alert"],
        index=0
    )
    messageUrgency = st.selectbox(
        "Message Urgency *",
        options=["low", "medium", "high", "critical"],
        index=1
    )
    messageBody = st.text_area("Message Body *", height=150)
    messengerID = st.number_input("Your User ID (Messenger ID) *", min_value=1, step=1)
    
    # Form submission button
    submitted = st.form_submit_button("Send Message")
    
    if submitted:
        # Validate required fields
        if not all([projectID, messageType, messageUrgency, messageBody, messengerID]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            message_data = {
                "messageType": messageType,
                "messageUrgency": messageUrgency,
                "messageBody": messageBody,
                "messengerID": messengerID
            }
            
            try:
                # Send POST request to API
                API_URL = f"http://web-api:4000/project_manager/projects/{projectID}/messages"
                response = requests.post(API_URL, json=message_data)
                
                if response.status_code == 201:
                    # Show success modal
                    result = response.json()
                    st.session_state.show_success_modal = True
                    st.session_state.success_message = f"Message sent successfully to {result.get('users_notified', 0)} users (Message ID: {result.get('messageID')})"
                    st.rerun()
                else:
                    st.error(
                        f"Failed to send message: {response.json().get('error', 'Unknown error')}"
                    )
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if message was sent successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_message)

# Add a button to return to the Project Manager Home
if st.button("Return to Project Manager Home", type="primary"):
    st.switch_page("pages/22_Project_Manager_Home.py")