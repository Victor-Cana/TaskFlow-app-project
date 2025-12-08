import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Resource Work Duration")

# Input for resource ID
resource_id = st.number_input("Enter Resource ID", min_value=1, step=1)

# Button to fetch work duration
if st.button("Get Work Duration", type="primary"):
    try:
        response = requests.get(f"http://web-api:4000/client_cfo/WorkSessions/{resource_id}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                st.success("Successfully retrieved work duration data!")
                
                # Display the result
                st.subheader("Work Duration Summary")
                st.metric(
                    label=f"Resource ID: {data.get('resourceID', 'N/A')}", 
                    value=f"{data.get('total_duration', '0')} hours"
                )
            else:
                st.warning("No work sessions found for this resource.")
                
        elif response.status_code == 404:
            st.warning("Duration not found for this resource.")
        else:
            st.error(f"Error fetching data: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add a button to return to the CFO Home
if st.button("Return to CFO Home"):
    st.switch_page("pages/10_Client_CFO_Home.py")