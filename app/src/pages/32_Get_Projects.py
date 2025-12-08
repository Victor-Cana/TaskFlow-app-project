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

st.title("User Projects")

# Input for user ID
user_id = st.number_input("Enter User ID", min_value=1, step=1)

# Function to show success dialog
def show_success_dialog(user_name):
    st.balloons()
    st.success(f"Successfully retrieved projects for {user_name}!")

# Button to fetch user projects
if st.button("Get User Projects"):
    try:
        response = requests.get(f"http://web-api:4000/team_member/users/{user_id}/projects")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                st.success("Successfully retrieved projects!")
                st.session_state.show_success_modal = True
                st.session_state.success_user_name = f"User {user_id}"
                
                # Display the results
                st.subheader("Projects")
                for project in data:
                    with st.expander(f"Project: {project.get('ProjectName', 'N/A')}"):
                        st.write(f"**Project ID:** {project.get('ProjectID', 'N/A')}")
                        st.write(f"**Description:** {project.get('Description', 'N/A')}")
                        st.write(f"**Due Date:** {project.get('DateDue', 'N/A')}")
            else:
                st.warning("No projects found for this user.")
        elif response.status_code == 404:
            st.error("User not found.")
        else:
            st.error(f"Error fetching data: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Show success modal if retrieval was successful
if st.session_state.get('show_success_modal', False):
    show_success_dialog(st.session_state.get('success_user_name', ''))

# Add a button to return to the Team Member Home
if st.button("Return to Team Member Home", type="primary"):
    st.session_state.show_success_modal = False
    st.switch_page("pages/30_Team_Member_Home.py")