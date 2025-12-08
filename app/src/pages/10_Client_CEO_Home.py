import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Client CEO, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What features would you like to test today?')

#create buttons for each of the features available to this user persona
if st.button('Pull Reports with Future Due Dates',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Get_Future_Reports.py')

if st.button('Create a New Project', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Create_Project.py')

if st.button('See Work Time for a Resource', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Resource_Time.py')

if st.button('Create a New Milestone', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_Create_Milestone')

if st.button('View Projects a User is Assigned To', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/15_Assigned_Resources')

if st.button('Pull Reports of a Specific Type', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/16_Get_Type_Reports')