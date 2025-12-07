import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Software Engineer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')


if st.button('Create a New Resource', 
             type='primary',
             use_container_width=True):
  st.switch_page('TaskFlowpages/01_Create_Resource.py')

if st.button('Update an Existing Resource', 
             type='primary',
             use_container_width=True):
  st.switch_page('TaskFlowpages/02_Update_Resource.py')

if st.button('Delete a Resource', 
             type='primary',
             use_container_width=True):
  st.switch_page('TaskFlowpages/03_Delete_Resource.py')

if st.button('Create a User', 
             type='primary',
             use_container_width=True):
  st.switch_page('TaskFlowpages/04_Create_User.py')