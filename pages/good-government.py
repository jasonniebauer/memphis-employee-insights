import streamlit as st
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data


##################################################
# Page initialization and setup
##################################################
st.set_page_config(
    page_title="Memphis Employee Insights – Good Government",
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
    [data-testid="stPageLink-NavLink"][href="good-government"] {
        background: #FEEFC3;
        border-left: 5px solid #FBBC04;
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
    st.title("Good Government")
    st.markdown('<h3 class="pt-0">Governance, Finance, HR, IT, and Legal</h3>', unsafe_allow_html=True)

    st.space()

    st.markdown('<h2 class="pt-0">Salaries by Division</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        st.markdown("[ PLACEHOLDER FOR PIE CHART]")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Governance</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        st.markdown("[ PLACEHOLDER FOR CHART]")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Finance</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        st.markdown("[ PLACEHOLDER FOR CHART]")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Human Resources</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        st.markdown("[ PLACEHOLDER FOR CHART]")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Information Technology</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        st.markdown("[ PLACEHOLDER FOR CHART]")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Legal</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        st.markdown("[ PLACEHOLDER FOR CHART]")

    # st.markdown(
    #     """
    #     **To do:**
    #     - ~~SECTION: Salaries by Division Category / Divisions~~
    #         - Total Salary of Good Government Workforce
    #         - Total Salaries by Division
    #         - Employee Workforce
    #             - Total full-time vs part-time employees across division category
    #             - Total employee breakdown by division
    #             - Percent of workforce by division
    #     - ~~SECTION: Governance~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: Finance~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: Human Resources~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: Information Technology~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: Legal~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     """
    # )