import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Team Member, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What features would you like to test today?')

#create buttons for each of the features available to this user persona
if st.button('Get Time Worked Info', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/31_Get_Worked_Time.py')

if st.button('Get all Projects Specific to a User', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/32_Get_Projects.py')

if st.button('Get all Deadlines', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/33_Get_Deadlines.py')

if st.button('Delete Resource Access for a User', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/34_Delete_Resource_Access.py')

if st.button('Get all Resources Associated With a Project', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/35_Get_Project_Resources.py')