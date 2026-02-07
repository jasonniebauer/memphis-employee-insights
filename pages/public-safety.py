import streamlit as st
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data


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

# Get data from session state
df = initialize_data()

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
    st.markdown("### Police, Fire, and Emergency Services")

    st.markdown(
        """
        **To do:**
        - SECTION: Salaries by Division Category / Divisions
            - Total Salary of Public Safety Workforce
            - Total Salaries by Division
            - Employee Workforce
                - Total full-time vs part-time employees across division category
                - Total employee breakdown by division
                - Percent of workforce by division
        - SECTION: Police Services
            - Employee Workforce
                - Total full-time vs part-time employees
            - Unique roles + average salary for role
            - Top paying position
            - Average salary across division
            - Average hourly rate across division (if applicable)
        - SECTION: Fire Services
            - Employee Workforce
                - Total full-time vs part-time employees
            - Unique roles + average salary for role
            - Top paying position
            - Average salary across division
            - Average hourly rate across division (if applicable)
        """
    )

    # # Filter to public safety departments
    # safety_depts = ['Police', 'Fire', 'EMS', '911 Communications']
    # safety_df = df[df['department'].isin(safety_depts)]

    # # Sidebar filters (page-specific)
    # with st.sidebar:
    #     st.markdown("---")
    #     st.subheader("Department Filters")
    #     selected_depts = st.multiselect(
    #         "Select Departments",
    #         # safety_depts,
    #         # default=safety_depts,
    #         df,
    #         default=df,
    #         # key="safety_dept_filter"
    #     )

    # # Apply filters
    # if selected_depts:
    #     safety_df = safety_df[safety_df['department'].isin(selected_depts)]

    # # Metrics
    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     st.metric("Total Employees", f"{len(safety_df):,}")

    # with col2:
    #     avg_salary = safety_df['salary'].mean()
    #     st.metric("Average Salary", f"${avg_salary:,.0f}")

    # with col3:
    #     total_cost = safety_df['salary'].sum()
    #     st.metric("Total Cost", f"${total_cost/1e6:.1f}M")

    # # Department breakdown
    # st.subheader("By Department")
    # dept_stats = safety_df.groupby('department').agg({
    #     'salary': ['count', 'mean', 'median']
    # }).round(0)
    # st.dataframe(dept_stats, use_container_width=True)

    # # Detailed data
    # with st.expander("View Employee Details"):
    #     st.dataframe(
    #         safety_df[['name', 'department', 'title', 'salary']].head(100),
    #         use_container_width=True,
    #         height=400
    #     )