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

#### ------------------------ Links for Role of Project Manager ------------------------
def ProjectManagerHomeNav():
    st.sidebar.page_link(
        "pages/22_Project_Manager_Home.py", label="Project Manager Home", icon="🏠"
    )

def CreateReportNav():
    st.sidebar.page_link(
        "pages/23_Create_Report.py", label="Create Report", icon="📝"
    )

def GrantResourceAccessNav():
    st.sidebar.page_link(
        "pages/24_Grant_Resource_Access.py", label="Grant Resource Access", icon="🔓"
    )

def RevokeResourceAccessNav():
    st.sidebar.page_link(
        "pages/25_Revoke_Resource_Access.py", label="Revoke Resource Access", icon="🔒"
    )

def AssignUserToProjectNav():
    st.sidebar.page_link(
        "pages/26_Assign_User_to_Project.py", label="Assign User to Project", icon="👤"
    )

def RemoveUserFromProjectNav():
    st.sidebar.page_link(
        "pages/27_Remove_User_from_Project.py", label="Remove User from Project", icon="👥"
    )

def SendProjectMessageNav():
    st.sidebar.page_link(
        "pages/28_Send_Project_Message.py", label="Send Project Message", icon="💬"
    )

def UpdateMessageNav():
    st.sidebar.page_link(
        "pages/29_Update_Message.py", label="Update Message", icon="✏️"
    )

def ViewProjectResourcesNav():
    st.sidebar.page_link(
        "pages/30_View_Project_Resources.py", label="View Project Resources", icon="📊"
    )

def ViewResourceWorkDurationNav():
    st.sidebar.page_link(
        "pages/31_View_Resource_Work_Duration.py", label="View Resource Work Duration", icon="⏱️"
    )


## ------------------------ Links for role of Client CFO ------------------------

def ClientCFOHomeNav():
    st.sidebar.page_link(
      "pages/10_Client_CFO_Home.py", label="Client CFO Home", icon="🏠"
    )

def FutureReportsNav():
    st.sidebar.page_link("pages/11_Get_Future_Reports.py", label="Future Reports", icon="📁")

def CreateNewProjectNav():
    st.sidebar.page_link('pages/12_Create_Project.py', label="Add New Project", icon="➕")

def ResourceWorkTimeNav():
    st.sidebar.page_link("pages/13_Resource_Time.py", label="Check Resource Work Time", icon="⏱️")

def CreateNewMilestoneNav():
    st.sidebar.page_link(
        "pages/14_Create_Milestone.py", label="Add New Milestone", icon="➕"
    )

def ViewUserProjectsNav():
    st.sidebar.page_link(
        'pages/15_Assigned_Resources.py', label="Check User Projects", icon="📦"
    )

def PullReportTypeNav():
     st.sidebar.page_link(
        'pages/16_Get_Type_Reports.py', label="Get Reports", icon="📁"
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

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "client_cfo":
            ClientCFOHomeNav()
            FutureReportsNav()
            CreateNewProjectNav()
            ResourceWorkTimeNav()
            CreateNewMilestoneNav()
            ViewUserProjectsNav()
            PullReportTypeNav()
            
        # If the user role is project_manager, show the project manager pages
        if st.session_state["role"] == "project_manager":
            ProjectManagerHomeNav()
            CreateReportNav()
            GrantResourceAccessNav()
            RevokeResourceAccessNav()
            AssignUserToProjectNav()
            RemoveUserFromProjectNav()
            SendProjectMessageNav()
            UpdateMessageNav()
            ViewProjectResourcesNav()
            ViewResourceWorkDurationNav()
            

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