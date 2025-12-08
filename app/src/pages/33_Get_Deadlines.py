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

st.title("Project Deadlines")

# Input for project ID
project_id = st.number_input("Enter Project ID", min_value=1, step=1)

# Optional filter by user ID
user_id = st.number_input("Filter by User ID (optional, 0 = no filter)", min_value=0, step=1)

# Function to show success dialog
def show_success_dialog(name):
    st.balloons()
    st.success(f"Successfully retrieved deadlines for {name}!")

# Button to fetch project deadlines
if st.button("Get Project Deadlines"):
    try:
        url = f"http://web-api:4000/team_member/projects/{project_id}/deadlines"
        if user_id > 0:
            url += f"?userID={user_id}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                st.success("Successfully retrieved deadlines!")
                st.session_state.show_success_modal = True
                st.session_state.success_user_name = f"Project {project_id}"
                
                # Display the results
                st.subheader("Upcoming Deadlines")
                for deadline in data:
                    days_until = deadline.get('DaysUntilDue', 0)
                    status = "🔴 Overdue" if days_until < 0 else "🟡 Due Soon" if days_until <= 3 else "🟢 On Track"
                    
                    with st.expander(f"{deadline.get('description', 'N/A')} - {status}"):
                        st.write(f"**Project:** {deadline.get('projectName', 'N/A')}")
                        st.write(f"**Due Date:** {deadline.get('dateDue', 'N/A')}")
                        st.write(f"**Date Done:** {deadline.get('dateDone', 'Not completed')}")
                        st.write(f"**Days Until Due:** {days_until}")
            else:
                st.warning("No deadlines found for this project.")
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