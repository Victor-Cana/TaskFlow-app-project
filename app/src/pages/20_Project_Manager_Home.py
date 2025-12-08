import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Project Manager, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

# Create buttons for each of the features available to this user persona
if st.button('Create a Report', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Create_Report.py')

if st.button('Grant Resource Access', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Grant_Resource_Access.py')

if st.button('Revoke Resource Access', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Revoke_Resource_Access.py')

if st.button('Assign User to Project', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/24_Assign_User_to_Project.py')

if st.button('Remove User from Project', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/25_Remove_User_from_Project.py')

if st.button('Send Project Message', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/26_Send_Project_Message.py')

if st.button('Update Message', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/27_Update_Message.py')

if st.button('View Project Resources', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/28_View_Project_Resources.py')

if st.button('View Resource Work Duration', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/29_View_Resource_Work_Duration.py')