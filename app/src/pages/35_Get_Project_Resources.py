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

st.title("Project Resources")

# Input for project ID
project_id = st.number_input("Enter Project ID", min_value=1, step=1)

# Function to show success dialog
def show_success_dialog(name):
    st.balloons()
    st.success(f"Successfully retrieved resources for {name}!")

# Button to fetch project resources
if st.button("Get Project Resources"):
    try:
        response = requests.get(f"http://web-api:4000/team_member/projects/{project_id}/resources")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                st.success("Successfully retrieved project and resources!")
                st.session_state.show_success_modal = True
                st.session_state.success_user_name = f"Project {project_id}"
                
                # Display project details
                st.subheader("Project Details")
                st.write(f"**Project Name:** {data.get('projectName', 'N/A')}")
                st.write(f"**Description:** {data.get('description', 'N/A')}")
                st.write(f"**Due Date:** {data.get('dateDue', 'N/A')}")
                
                # Display resources
                st.subheader("Associated Resources")
                resources = data.get('resources', [])
                
                if resources:
                    for resource in resources:
                        with st.expander(f"Resource: {resource.get('resourceName', 'N/A')}"):
                            st.write(f"**Resource ID:** {resource.get('resourceID', 'N/A')}")
                            st.write(f"**Type:** {resource.get('resourceType', 'N/A')}")
                            st.write(f"**Description:** {resource.get('description', 'N/A')}")
                else:
                    st.info("No resources associated with this project.")
            else:
                st.warning("No data found for this project.")
        elif response.status_code == 404:
            st.error("Project not found.")
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

    