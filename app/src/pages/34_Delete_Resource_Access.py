import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize session state FIRST
if 'show_success_modal' not in st.session_state:
    st.session_state.show_success_modal = False
if 'success_user_name' not in st.session_state:
    st.session_state.success_user_name = ""

# Initialize sidebar
SideBarLinks()

st.title("Remove Resource Access")

st.warning("⚠️ This action will permanently remove a user's access to a resource.")

# Input for user ID and resource ID
user_id = st.number_input("Enter User ID", min_value=1, step=1)
resource_id = st.number_input("Enter Resource ID", min_value=1, step=1)

# Function to show success dialog
def show_success_dialog(name):
    st.balloons()
    st.success(f"Successfully removed access: {name}!")

# Button to remove access
if st.button("Remove Access", type="primary"):
    try:
        response = requests.delete(f"http://web-api:4000/team_member/haveaccessto/{user_id}/{resource_id}")
        
        if response.status_code == 200:
            st.success("Successfully removed resource access!")
            st.session_state.show_success_modal = True
            st.session_state.success_user_name = f"User {user_id} from Resource {resource_id}"
            
        elif response.status_code == 404:
            st.error("Access record not found. This user may not have access to this resource.")
        else:
            st.error(f"Error removing access: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Show success modal if removal was successful
if st.session_state.get('show_success_modal', False):
    show_success_dialog(st.session_state.get('success_user_name', ''))

# Add a button to return to the Team Member Home
if st.button("Return to Team Member Home", type="primary"):
    st.session_state.show_success_modal = False
    st.switch_page("pages/30_Team_Member_Home.py")