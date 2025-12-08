import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("View Project Resources")

# Input for project ID
projectID = st.number_input("Enter Project ID", min_value=1, step=1, key="project_id_input")

if st.button("Load Resources", type="primary"):
    if projectID:
        try:
            # API endpoint
            API_URL = f"http://web-api:4000/project_manager/projects/{projectID}/resources"
            
            # Fetch resources from backend
            response = requests.get(API_URL)
            
            if response.status_code == 200:
                resources = response.json()
                
                if resources:
                    st.success(f"Found {len(resources)} resources for Project #{projectID}")
                    
                    # Convert to DataFrame for better display
                    df = pd.DataFrame(resources)
                    
                    # Select relevant columns to display
                    columns_to_display = ['resourceID', 'name', 'type', 'description', 'link', 'dateDue']
                    df_display = df[[col for col in columns_to_display if col in df.columns]]
                    
                    # Display as a table
                    st.dataframe(df_display, use_container_width=True, hide_index=True)
                    
                else:
                    st.info(f"No resources found for Project #{projectID}")
            else:
                st.error(f"Failed to load resources: {response.json().get('error', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")
            st.info("Please ensure the API server is running")
    else:
        st.warning("Please enter a valid Project ID")

# Add a button to return to the Project Manager Home
st.write("")
if st.button("Return to Project Manager Home", type="secondary"):
    st.session_state.show_success_modal = False
    st.switch_page("pages/20_Project_Manager_Home.py")