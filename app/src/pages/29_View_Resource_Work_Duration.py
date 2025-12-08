import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("View Resource Work Duration")

st.write("This page shows the total work duration for each resource across all work sessions.")

if st.button("Load Work Durations", type="primary"):
    try:
        # API endpoint
        API_URL = "http://web-api:4000/project_manager/resources/work-duration"
        
        # Fetch work durations from backend
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            durations = response.json()
            
            if durations:
                st.success(f"Found work duration data for {len(durations)} resources")
                
                df = pd.DataFrame(durations)
                
                # Convert seconds to hours and rename column
                df['total_duration'] = pd.to_numeric(df['total_duration'], errors='coerce') 
                df['Total Hours Worked'] = df['total_duration'] / 3600
                df = df[['resourceID', 'Total Hours Worked']]  
                
                # Display as a table
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Display a bar chart with horizontal labels
                if len(durations) > 0:
                    st.write("### Duration Visualization")
                    
                    # Set resourceID as string (For Display)
                    chart_data = df.copy()
                    chart_data['resourceID'] = chart_data['resourceID'].astype(str)
                    chart_data = chart_data.set_index('resourceID')
                    
                    st.bar_chart(chart_data)
                
            else:
                st.info("No work duration data available")
        else:
            st.error(f"Failed to load work durations: {response.json().get('error', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running")

# Add a button to return to the Project Manager Home
st.write("")
if st.button("Return to Project Manager Home", type="secondary"):
    if "show_success_modal" in st.session_state:
        st.session_state.show_success_modal = False
    st.switch_page("pages/22_Project_Manager_Home.py")