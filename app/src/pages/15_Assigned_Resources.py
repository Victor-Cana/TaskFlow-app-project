import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
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

# Button to fetch projects
if st.button("Get User Projects"):
    try:
        response = requests.get(f"http://web-api:4000/client_cfo/assignedto/{user_id}")
        
        if response.status_code == 200:
            projects = response.json()
            
            if projects:
                st.success(f"Successfully retrieved {len(projects)} project(s)!")
                st.session_state.show_success_modal = True
                st.session_state.success_user_name = f"User {user_id}"
                
                # Display the results
                st.subheader(f"Projects for User {user_id}")
                
                for project in projects:
                    with st.expander(f"📁 {project.get('projectName', 'Untitled Project')} (ID: {project.get('projectID')})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Project ID:** {project.get('projectID')}")
                            st.write(f"**Due Date:** {project.get('dateDue', 'N/A')}")
                            st.write(f"**Access Level:** {project.get('accessLevel', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Date Assigned:** {project.get('dateAssigned', 'N/A')}")
                            if project.get('description'):
                                st.write(f"**Description:** {project.get('description')}")
            else:
                st.warning("No projects found for this user.")
        elif response.status_code == 404:
            st.warning("No projects found for this user.")
        else:
            st.error(f"Error fetching data: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Show success modal if getting project count was successful
if st.session_state.get('show_success_modal', False):
    show_success_dialog(st.session_state.get('success_user_name', ''))

# Add a button to return to the CFO Home
if st.button("Return to CFO Home", type="primary"):
    st.switch_page("pages/10_Client_CFO_Home.py")