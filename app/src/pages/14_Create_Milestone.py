import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Future Reports")

# Button to fetch future reports
if st.button("Get Future Reports", type="primary"):
    try:
        response = requests.get("http://web-api:4000/client_cfo/reports")
        
        if response.status_code == 200:
            reports = response.json()
            
            if reports:
                st.success(f"Successfully retrieved {len(reports)} report(s) with future due dates!")
                
                # Display each report
                for report in reports:
                    with st.expander(f"Report: {report.get('title', 'Untitled')}"):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Report Details")
                            for key, value in report.items():
                                st.write(f"**{key.title()}:** {value}")
            else:
                st.warning("No reports with future due dates found.")
                
        elif response.status_code == 404:
            st.warning("No reports found with future due dates.")
        else:
            st.error(f"Error fetching data: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add a button to return home (adjust the page path as needed)
if st.button("Return to CFO Home"):
    st.switch_page("pages/10_Client_CFO_Home.py")  