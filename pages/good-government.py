import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
from shared.colors import ORANGE, YELLOW, LIGHT_YELLOW


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

# Get data from session state
df = initialize_data()

# # Good Government divisions
# good_government_divisions = [
#     'Executive',
#     'Finance and Administration',
#     'Human Resources',
#     'Information Technology',
#     'City Attorney',
#     'City Court Clerk',
#     'Legislative',
#     'Judicial',
# ]

# Filter DataFrame to Good Government divisions
# df = df[df['Division Name'].isin(good_government_divisions)]
df = df[df['Division Category'] == 'Good Government']

def get_category(row):
    division = row['Division Name']
    governance = ['Executive', 'Legislative', 'Judicial']
    legal = ['City Attorney', 'City Court Clerk']

    if division in governance:
        return 'Governance'
    elif division in legal:
        return 'Legal'
    elif division == 'Finance and Administration':
        return 'Finance'
    elif division == 'Human Resources':
        return 'HR'
    elif division == 'Information Technology':
        return 'IT'
    else:
        return

# Define category to group divisions
df['Category'] = df.apply(get_category, axis=1)

# Calculating the sum of all salaries in each division
division_salary_totals = pd.DataFrame(
    df.groupby('Category')['Annual Salary'].sum()
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
    st.title("Good Government")
    st.markdown('<h3 class="pt-0">Finance, HR, IT, Legal, and Governance</h3>', unsafe_allow_html=True)

    st.space()

    st.markdown('<h2 class="pt-0">Salaries by Division</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        # Define colors
        color_map = {
            "Governance": ORANGE,
            "Finance": YELLOW,
            "Legal": LIGHT_YELLOW,
            'HR': '#FFCC80',
            'IT': '#FF9800'
        }

        pie_chart_job_category = alt.Chart(division_salary_totals).mark_arc().encode(
            theta="Annual Salary:Q",
            color=alt.Color(
                "Category:N",
                title="Category",
                scale=alt.Scale(
                    domain=list(color_map.keys()),
                    range=list(color_map.values())
                )
            ),
            tooltip=[
                "Category",
                alt.Tooltip("Annual Salary:Q", format="$,.2f", title="Salaries"),
                alt.Tooltip("Percentage:Q", format=".1%", title="Percentage")
            ]
        )

        st.altair_chart(pie_chart_job_category, width="stretch")

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