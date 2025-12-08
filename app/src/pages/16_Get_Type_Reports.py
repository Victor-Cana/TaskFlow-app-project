import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize session state FIRST
if 'show_success_modal' not in st.session_state:
    st.session_state.show_success_modal = False
if 'success_report_type' not in st.session_state:
    st.session_state.success_report_type = ""

# Initialize sidebar
SideBarLinks()

st.title("Reports by Type")

# Text input for report type
report_type = st.text_input("Enter Report Type (e.g., Financial, Process, Technical, Update)")

# Function to show success dialog
def show_success_dialog(type_name):
    st.balloons()
    st.success(f"Successfully retrieved {type_name} reports!")

# Button to fetch reports
if st.button("Get Reports"):
    if not report_type:
        st.error("Please enter a report type")
    else:
        try:
            response = requests.get(f"http://web-api:4000/client_cfo/reports/{report_type}")
            
            if response.status_code == 200:
                reports = response.json()
                
                if reports:
                    st.success(f"Successfully retrieved {len(reports)} {report_type} report(s)!")
                    st.session_state.show_success_modal = True
                    st.session_state.success_report_type = report_type
                    
                    # Display the results
                    st.subheader(f"{report_type} Reports")
                    
                    for report in reports:
                        with st.expander(f"📊 Report ID: {report.get('reportID')} - Project {report.get('projectID')}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Report ID:** {report.get('reportID')}")
                                st.write(f"**Project ID:** {report.get('projectID')}")
                                st.write(f"**Type:** {report.get('type')}")
                                st.write(f"**Resource Count:** {report.get('resourceCount', 0)}")
                            
                            with col2:
                                st.write(f"**Due Date:** {report.get('dateDue', 'N/A')}")
                                st.write(f"**Date Done:** {report.get('dateDone', 'Not completed')}")
                                if report.get('description'):
                                    st.write(f"**Description:** {report.get('description')}")
                else:
                    st.warning(f"No {report_type} reports found.")
            elif response.status_code == 404:
                st.warning(f"No {report_type} reports found.")
            else:
                st.error(f"Error fetching data: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure the backend is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Show success modal if getting reports was successful
if st.session_state.get('show_success_modal', False):
    show_success_dialog(st.session_state.get('success_report_type', ''))

# Add a button to return to the CFO Home
if st.button("Return to CFO Home", type="primary"):
    st.switch_page("pages/10_Client_CFO_Home.py")