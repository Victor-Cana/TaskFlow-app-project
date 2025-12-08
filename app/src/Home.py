##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('Welcome to TaskFlow!')
st.write('\n\n')
# st.write('### Overview:')
# st.write('\n')
st.write('#### Select the user you would like to log in as.')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Login as Kyle Wilson, a Software Engineer at TaskFlow", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'software_engineer'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Kyle'
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Software Engineer Persona")
    st.switch_page('pages/00_Software_Engineer_Home.py')

if st.button('Act as John Kraft, a CFO of a TaskFlow client', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'client_cfo'
    st.session_state['first_name'] = 'John'
    st.switch_page('pages/10_Client_CFO_Home.py')

if st.button('Act as Evan Park, a Student Group Project Manager', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'project_manager'
    st.session_state['first_name'] = 'Evan'
    st.switch_page('pages/20_Project_Manager_Home.py')

if st.button('Act as Ryan Kim, a Student Team Member', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'team_member'
    st.session_state['first_name'] = 'Ryan'
    st.switch_page('pages/30_Team_Member_Home.py')

