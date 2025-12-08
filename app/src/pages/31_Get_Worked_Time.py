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

st.title("Time Logged")

# Input for resource ID
resource_id = st.number_input("Enter Resource ID", min_value=1, step=1)

# Function to show success dialog
def show_success_dialog(user_name):
    st.balloons()
    st.success(f"Successfully retrieved time worked for {user_name}!")

# Button to fetch time worked
if st.button("Get Time Worked"):
    try:
        response = requests.get(f"http://web-api:4000/team_member/worksessions/{resource_id}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                st.success("Successfully retrieved time data!")
                st.session_state.show_success_modal = True
                st.session_state.success_user_name = f"Resource {resource_id}"
                
                # Display the results
                st.subheader("Time Worked Summary")
                for record in data:
                    st.metric(
                        label=f"Resource ID: {record['resourceID']}", 
                        value=f"{record['total_duration']} hours"
                    )
            else:
                st.warning("No work sessions found for this resource.")
        else:
            st.error(f"Error fetching data: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Show success modal if getting work time was successful
if st.session_state.get('show_success_modal', False):
    show_success_dialog(st.session_state.get('success_user_name', ''))

# Add a button to return to the Team Member Home
if st.button("Return to Team Member Home", type="primary"):
    st.switch_page("pages/30_Team_Member_Home.py")
