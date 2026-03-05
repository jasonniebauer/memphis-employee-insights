import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
from shared.processing import get_division_details
from shared.utilities import employment_type_table, employment_type_pie_chart
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
st.markdown(
    """
    <style>
        /* Set background color for active page link */
        [data-testid="stPageLink-NavLink"][href="public-safety"] {
            background: #FAD2CF;
            border-left: 5px solid #EA4335;
            padding-left: 0.2rem;
        }

        [data-testid="stMetricDelta"] {
            background: #FAD2CF !important;
            color: #202124 !important;
        }
    </style>
    """, unsafe_allow_html=True
)

##################################################
# Data Preparation
##################################################

# Get data from session state
df = initialize_data()

# # Public Safety divisions
# public_safety_divisions = ['Police Services', 'Fire Services']
# df = df[df['Division Name'].isin(public_safety_divisions)]

# Filter DataFrame to Public Safety divisions
df = df[df['Division Category'] == 'Public Safety']

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

# # Calculate division salary percentage of total
# division_salary_totals['Percentage'] = (
#     division_salary_totals['Annual Salary'] / division_salary_totals['Annual Salary'].sum()
# )

# Get the total salary of Public Safety workforce (in millions)
public_safety_total_salary = df['Annual Salary'].sum() / 1e6

# Get total number of employees
total_employees = len(df)
# Get total number of full-time employees
total_full_time_employees = (df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_employees = (df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing division category's employees by employment type
employment_type_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [total_full_time_employees / total_employees, total_part_time_employees / total_employees],
    "Count": [total_full_time_employees, total_part_time_employees]
})

(
    top_paying_police_job,
    max_police_salary,
    min_police_salary,
    top_paying_police_part_time_job,
    max_police_hourly_rate,
    min_police_hourly_rate,
    average_police_salary,
    average_police_hourly_rate,
    total_unique_police_jobs,
    total_police_employees,
    total_full_time_police_employees,
    total_part_time_police_employees,
    employment_type_police_totals_df
) = get_division_details('Police Services')

(
    top_paying_fire_job,
    max_fire_salary,
    min_fire_salary,
    top_paying_fire_part_time_job,
    max_fire_hourly_rate,
    min_fire_hourly_rate,
    average_fire_salary,
    average_fire_hourly_rate,
    total_unique_fire_jobs,
    total_fire_employees,
    total_full_time_fire_employees,
    total_part_time_fire_employees,
    employment_type_fire_totals_df
) = get_division_details('Fire Services')

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

        st.markdown(
            """
            <div class="table-row">
                <span class="bold">Division</span>
                <span class="bold">Percent of Public Safety Salaries</span>
            </div>
            <div class="table-row">
                <span>Police Services</span>
                <span>57.7%</span>
            </div>
            <div class="table-row"">
                <span>Fire Services</span>
                <span>42.3%</span>
            </div>
            <div class="table-row">
                <span class="bold">Total</span>
                <span class="bold">100%</span>
            </div>
            """, unsafe_allow_html=True
        )

        st.space()

        st.metric(
            label=":material/local_police: Public Safety Workforce Salaries",
            value=f"${public_safety_total_salary:,.1f}M",  
            delta=None,
        )

    with salary_cols[1]:
        chart = alt.Chart(division_salary_totals).mark_bar(color=MEDIUM_RED).encode(
            x=alt.X(
                'Division Name',
                axis=alt.Axis(labelAngle=0),  # Rotate labels
                sort=None,
                title=None,
            ),
            y=alt.Y(
                'Annual Salary',
                axis=alt.Axis(
                    title='Annual Salary Total',
                    format='$,s'  # Format numbers
                ),
            ),
            tooltip=[
                alt.Tooltip("Division Name:N", title="Division"),
                alt.Tooltip("Annual Salary:Q", format="$,.2f", title="Salaries")
            ]
        )

        st.altair_chart(chart)

    st.space()

    st.markdown('### Employment Breakdown')
    
    salary_row2_cols = st.columns(2, gap="xlarge")

    with salary_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_employees,
                total_part_time_employees,
                total_employees
            ),
            unsafe_allow_html=True
        )

    with salary_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_totals_df,
            MEDIUM_RED,
            LIGHT_RED
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")
    
    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Police Services</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.text(
            f"""
            Salaries in the Memphis Police Department range widely. They start from a low of roughly ${round(min_police_salary, -3):,.0f} annually for certain support or entry-level non-sworn roles (such as Communication Safety Equipment Installer). They extend upward through career progression in sworn and specialized roles, with top earners in supervisory, command, and leadership positions exceeding ${round(max_police_salary, -3):,.0f} per year.
            
            Part-time or hourly support roles often start around $12 per hour, while some specialized or higher-skilled part-time/contract positions can reach up to $50 per hour depending on the role. 
            """
        )

        st.markdown(
            f"""
            <div class="table-row"">
                <span class="bold">Average salary (full-time)</span>
                <span>${average_police_salary:,.2f}</span>
            </div>
            <div class="table-row"">
                <span class="bold">Average hourly rate (part-time)</span>
                <span>${average_police_hourly_rate:,.2f}</span>
            </div>
            """, unsafe_allow_html=True
        )

    with salary_cols[1]:
        st.metric(
            label=f":material/local_police: {top_paying_police_job}".replace("Svcs", "Services"),
            value=f"${max_police_salary/1e3:,.1f}k",  
            delta="Top Full-Time Salary",
        )
        st.space()
        st.metric(
            label=f":material/assignment: {top_paying_police_part_time_job}",
            value=f"${max_police_hourly_rate:.0f}/hr",  
            delta="Top Part-Time Rate",
        )

    st.space()

    st.markdown('### Police Services Employment Breakdown')
    
    police_row2_cols = st.columns(2, gap="xlarge")

    with police_row2_cols[0]:
        st.markdown(
            f"""
            The Police Services workforce is made up of {total_unique_police_jobs} unique roles
            with the the majority (77) of jobs being offered as full-time whereas a smaller portion (17) are offered as part-time, hourly roles.
            """
        )
        st.markdown(
            employment_type_table(
                total_full_time_police_employees,
                total_part_time_police_employees,
                total_police_employees
            ),
            unsafe_allow_html=True
        )

    with police_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_police_totals_df,
            MEDIUM_RED,
            LIGHT_RED
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")
    
    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Fire Services</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown(
            f"""Salaries for full-time employees range from ${min_fire_salary/1e3:,.1f}k to {max_fire_salary/1e3:,.1f}k annually."""
        )

        st.markdown(
            f"""
            <div class="table-row"">
                <span class="bold">Average salary</span>
                <span>${average_fire_salary:,.2f}</span>
            </div>
            <div class="table-row"">
                <span class="bold">Average hourly rate</span>
                <span>${average_fire_hourly_rate:,.2f}</span>
            </div>
            <div class="table-row">
                <span class="bold">Unique jobs</span>
                <span>{total_unique_fire_jobs}</span>
            </div>
            """, unsafe_allow_html=True
        )

    with salary_cols[1]:
        st.metric(
            label=f":material/local_fire_department: {top_paying_fire_job}".replace("Svcs", "Services"),
            value=f"${max_fire_salary/1e3:,.1f}k",  
            delta="Top Full-Time Salary",
        )

        st.metric(
            label=f":material/health_and_safety: {top_paying_fire_part_time_job}".replace("RN", "Registered Nurse").replace("Oper", "Operator"),
            value=f"${max_fire_hourly_rate:.0f}/hr",  
            delta="Top Part-Time Rate",
        )

    st.space()

    st.markdown('### Fire Services Employment Breakdown')
    
    fire_row2_cols = st.columns(2, gap="xlarge")

    with fire_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_fire_employees,
                total_part_time_fire_employees,
                total_fire_employees
            ),
            unsafe_allow_html=True
        )

    with fire_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_fire_totals_df,
            MEDIUM_RED,
            LIGHT_RED
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    # st.markdown(
    #     """
    #     **To do:**
    #     - ~~SECTION: Salaries by Division Category / Divisions~~
    #         - ~~Total Salary of Public Safety Workforce~~
    #         - Total Salaries by Division
    #         - Employee Workforce
    #             - ~~Total full-time vs part-time employees across division category~~
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