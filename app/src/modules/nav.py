# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/40_About.py", label="About", icon="🧠")


#### ------------------------ Links for Role of Software Engineer ------------------------
def SoftwareEngineerHomeNav():
    st.sidebar.page_link(
        "pages/00_Software_Engineer_Home.py", label="Software Engineer Home", icon="🏠"
    )


def CreateResourceNav():
    st.sidebar.page_link(
        "pages/01_Create_Resource.py", label="Create Resource", icon="➕"
    )

def UpdateResourceNav():
    st.sidebar.page_link(
        "pages/02_Update_Resource.py", label="Update Resource", icon="🔄"
    )

def DeleteResourceNav():
    st.sidebar.page_link(
        "pages/03_Delete_Resource.py", label="Delete Resource", icon="❌"
    )

def CreateUserNav():
    st.sidebar.page_link(
        "pages/04_Create_User.py", label="Create User", icon="➕"
    )

#### ------------------------ Links for Role of Team Member ------------------------
def TeamMemberHomeNav():
    st.sidebar.page_link(
        "pages/30_Team_Member_Home.py", label="Team Member Home", icon="🏠"
    )

def GetWorkedTimeNav():
    st.sidebar.page_link(
        "pages/31_Get_Worked_Time.py", label="Get Worked Time", icon="⏱️"
    )

def UserProjectsNav():
    st.sidebar.page_link(
        "pages/32_Get_Projects.py", label="User Projects", icon="📁"
    )

def ProjectDeadlinesNav():
    st.sidebar.page_link(
        "pages/33_Get_Deadlines.py", label="Project Deadlines", icon="📅"
    )

def RemoveResourceAccessNav():
    st.sidebar.page_link(
        "pages/34_Delete_Resource_Access.py", label="Remove Resource Access", icon="🚫"
    )

def ProjectResourcesNav():
    st.sidebar.page_link(
        "pages/35_Get_Project_Resources.py", label="Project Resources", icon="📦"
    )

## ------------------------ Examples for Role of usaid_worker ------------------------

def usaidWorkerHomeNav():
    st.sidebar.page_link(
      "pages/10_USAID_Worker_Home.py", label="USAID Worker Home", icon="🏠"
    )

def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")

def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")

def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")

def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )

def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )





#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/TaskFlowTransparentBackground.png", width=200)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "software_engineer":
            SoftwareEngineerHomeNav()
            CreateResourceNav()
            UpdateResourceNav()
            DeleteResourceNav()
            CreateUserNav()

        # Add this section for Team Member
        if st.session_state['role'] == 'team_member':
            TeamMemberHomeNav()
            GetWorkedTimeNav()
            UserProjectsNav()
            ProjectDeadlinesNav()
            RemoveResourceAccessNav()
            ProjectResourcesNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "usaid_worker":
            usaidWorkerHomeNav()
            NgoDirectoryNav()
            AddNgoNav()
            PredictionNav()
            ApiTestNav()
            ClassificationNav()
            

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
    
    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
