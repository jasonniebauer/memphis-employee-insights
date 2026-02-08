import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
from shared.colors import MEDIUM_RED, LIGHT_RED


##################################################
# Page initialization and setup
##################################################
st.set_page_config(
    page_title="Memphis Employee Insights – Public Safety",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render navigation
render_navigation()

# Render reusable styles
render_reusable_styles()

# Page-specific CSS (only runs here on page)
st.markdown("""
<style>
    /* Set background color for active page link */
    [data-testid="stPageLink-NavLink"][href="public-safety"] {
        background: #FAD2CF;
        border-left: 5px solid #EA4335;
        padding-left: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

##################################################
# Data Preparation
##################################################

# Get data from session state
df = initialize_data()

# Public Safety divisions
public_safety_divisions = ['Police Services', 'Fire Services']
# Filter DataFrame to Public Safety divisions
df = df[df['Division Name'].isin(public_safety_divisions)]

# Calculating the sum of all salaries in each division
division_salary_totals = pd.DataFrame(
    df.groupby('Division Name')['Annual Salary'].sum()
).reset_index()

# Sort divisions by the sum of all salaries in descending order
division_salary_totals.sort_values(
    by='Annual Salary',
    ascending=False,
    inplace=True
)

# Calculate division salary percentage of total
division_salary_totals['Percentage'] = (
    division_salary_totals['Annual Salary'] / division_salary_totals['Annual Salary'].sum()
)

##################################################
# UI Content
##################################################

st.space()

with st.spinner('Loading data and calculations...'):
    st.info(
        'Building Better Transparency: Under Active Development – Check Back for More Soon!',
        icon=":material/build:"
    )
    st.title("Public Safety")
    st.markdown('<h3 class="pt-0">Police, Fire, and Emergency Services</h3>', unsafe_allow_html=True)

    st.space()

    st.markdown('<h2 class="pt-0">Salaries by Division</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        # Define colors
        color_map = {
            "Police Services": MEDIUM_RED,
            "Fire Services": LIGHT_RED
        }

        pie_chart_job_category = alt.Chart(division_salary_totals).mark_arc().encode(
            theta="Annual Salary:Q",
            color=alt.Color(
                "Division Name:N",
                title="Division",
                scale=alt.Scale(
                    domain=list(color_map.keys()),
                    range=list(color_map.values())
                )
            ),
            tooltip=[
                "Division Name",
                alt.Tooltip("Annual Salary:Q", format="$,.2f", title="Salaries"),
                alt.Tooltip("Percentage:Q", format=".1%", title="Percentage")
            ]
        )

        st.altair_chart(pie_chart_job_category, width="stretch")
    
    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Police Services</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        st.markdown("[ PLACEHOLDER FOR CHART]")
    
    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Fire Services</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        st.markdown("[ PLACEHOLDER FOR CHART]")

    # st.markdown(
    #     """
    #     **To do:**
    #     - ~~SECTION: Salaries by Division Category / Divisions~~
    #         - Total Salary of Public Safety Workforce
    #         - Total Salaries by Division
    #         - Employee Workforce
    #             - Total full-time vs part-time employees across division category
    #             - Total employee breakdown by division
    #             - Percent of workforce by division
    #     - ~~SECTION: Police Services~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: Fire Services~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     """
    # )