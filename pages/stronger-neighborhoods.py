import streamlit as st
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data


##################################################
# Page initialization and setup
##################################################
st.set_page_config(
    page_title="Memphis Employee Insights – Stronger Neighborhoods",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render navigation
render_navigation()

# Render reusable styles
render_reusable_styles()

# Get data from session state
df = initialize_data()

# Page-specific CSS (only runs here on page)
st.markdown("""
<style>
    /* Set background color for active page link */
    [data-testid="stPageLink-NavLink"][href="stronger-neighborhoods"] {
        background: #CEEAD6;
        border-left: 5px solid #34A853;
        padding-left: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

##################################################
# Data Preparation
##################################################

##################################################
# UI Content
##################################################
st.space()

with st.spinner('Loading data and calculations...'):
    st.info(
        'Building Better Transparency: Under Active Development – Check Back for More Soon!',
        icon=":material/build:"
    )
    st.title("Stronger Neighborhoods")
    st.markdown("### Parks, Libraries, and Housing & Community Development")

    st.markdown(
        """
        **To do:**
        - SECTION: Salaries by Division Category / Divisions
            - Total Salary of Stronger Neighborhoods Workforce
            - Total Salaries by Division
            - Employee Workforce
                - Total full-time vs part-time employees across division category
                - Total employee breakdown by division
                - Percent of workforce by division
        - SECTION: Parks
            - Employee Workforce
                - Total full-time vs part-time employees
            - Unique roles + average salary for role
            - Top paying position
            - Average salary across division
            - Average hourly rate across division (if applicable)
        - SECTION: Libraries
            - Employee Workforce
                - Total full-time vs part-time employees
            - Unique roles + average salary for role
            - Top paying position
            - Average salary across division
            - Average hourly rate across division (if applicable)
        - SECTION: Housing & Community Development
            - Employee Workforce
                - Total full-time vs part-time employees
            - Unique roles + average salary for role
            - Top paying position
            - Average salary across division
            - Average hourly rate across division (if applicable)
        """
    )