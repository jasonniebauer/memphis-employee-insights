import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
from shared.processing import get_division_details
from shared.utilities import employment_type_table, employment_type_pie_chart
from shared.colors import MEDIUM_GREEN, LIGHT_GREEN


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

# Get data from session state
df = initialize_data()

# Filter DataFrame to Stronger Neighborhood divisions
df = df[df['Division Category'] == 'Stronger Neighborhoods']

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

# Get the total salary of Stronger Neighborhoods workforce (in millions)
stronger_neighborhoods_total_salary = df['Annual Salary'].sum() / 1e6

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

# Make a copy of the original DataFrame
memphis_parks_df = df.copy()
# Filter employees to only those in Memphis Parks
memphis_parks_df = memphis_parks_df[memphis_parks_df['Division Name'] == 'Memphis Parks']

# Get total number of Memphis Parks employees
total_memphis_parks_employees = len(memphis_parks_df)
# Get total number of full-time employees
total_full_time_memphis_parks_employees = (memphis_parks_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_memphis_parks_employees = (memphis_parks_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Memphis Parks employees by employment type
employment_type_memphis_parks_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_memphis_parks_employees / total_memphis_parks_employees,
        total_part_time_memphis_parks_employees / total_memphis_parks_employees
    ],
    "Count": [
        total_full_time_memphis_parks_employees,
        total_part_time_memphis_parks_employees
    ]
})

# Make a copy of the original DataFrame
library_df = df.copy()
# Filter employees to only those in Library Services
library_df = library_df[library_df['Division Name'] == 'Library Services']

# Get total number of Library Services employees
total_library_employees = len(library_df)
# Get total number of full-time employees
total_full_time_library_employees = (library_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_library_employees = (library_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Library Servicess employees by employment type
employment_type_library_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_library_employees / total_library_employees,
        total_part_time_library_employees / total_library_employees
    ],
    "Count": [
        total_full_time_library_employees,
        total_part_time_library_employees
    ]
})

# Make a copy of the original DataFrame
housing_df = df.copy()
# Filter employees to only those in Housing and Community Development
housing_df = housing_df[housing_df['Division Name'] == 'Housing and Community Development']

# Get total number of Housing and Community Development employees
total_housing_employees = len(housing_df)
# Get total number of full-time employees
total_full_time_housing_employees = (housing_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_housing_employees = (housing_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Housing and Community Development employees by employment type
employment_type_housing_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_housing_employees / total_housing_employees,
        total_part_time_housing_employees / total_housing_employees
    ],
    "Count": [
        total_full_time_housing_employees,
        total_part_time_housing_employees
    ]
})

(
    top_paying_memphis_parks_job,
    max_memphis_parks_salary,
    min_memphis_parks_salary,
    top_paying_memphis_parks_part_time_job,
    max_memphis_parks_hourly_rate,
    min_memphis_parks_hourly_rate,
    average_memphis_parks_salary,
    average_memphis_parks_hourly_rate,
    total_unique_memphis_parks_jobs,
    total_memphis_parks_employees,
    total_full_time_memphis_parks_employees,
    total_part_time_memphis_parks_employees,
    employment_type_memphis_parks_totals_df
) = get_division_details('Memphis Parks')

(
    top_paying_library_services_job,
    max_library_services_salary,
    min_library_services_salary,
    top_paying_library_services_part_time_job,
    max_library_services_hourly_rate,
    min_library_services_hourly_rate,
    average_library_services_salary,
    average_library_services_hourly_rate,
    total_unique_library_services_jobs,
    total_library_services_employees,
    total_full_time_library_services_employees,
    total_part_time_library_services_employees,
    employment_type_library_services_totals_df
) = get_division_details('Library Services')

(
    top_paying_housing_community_job,
    max_housing_community_salary,
    min_housing_community_salary,
    top_paying_housing_community_part_time_job,
    max_housing_community_hourly_rate,
    min_housing_community_hourly_rate,
    average_housing_community_salary,
    average_housing_community_hourly_rate,
    total_unique_housing_community_jobs,
    total_housing_community_employees,
    total_full_time_housing_community_employees,
    total_part_time_housing_community_employees,
    employment_type_housing_community_totals_df
) = get_division_details('Housing and Community Development')

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
    st.markdown('<h3 class="pt-0">Parks, Libraries, and Housing & Community Development</h3>', unsafe_allow_html=True)

    st.space()

    st.markdown('<h2 class="pt-0">Salaries by Division</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            """
            <div class="table-row">
                <span class="bold">Division</span>
                <span class="bold">Percent of Stronger Neighborhood Salaries</span>
            </div>
            <div class="table-row">
                <span>Memphis Parks</span>
                <span>42.7%</span>
            </div>
            <div class="table-row"">
                <span>Library Services</span>
                <span>42.2%</span>
            </div>
            <div class="table-row"">
                <span>Housing and Community Development</span>
                <span>15.1%</span>
            </div>
            <div class="table-row">
                <span class="bold">Total</span>
                <span class="bold">100%</span>
            </div>
            """, unsafe_allow_html=True
        )

        st.space()

        st.metric(
            label=":material/psychiatry: Stronger Neighborhoods Workforce Salaries",
            value=f"${stronger_neighborhoods_total_salary:,.1f}M",  
            delta=None,
        )

    with salary_cols[1]:
        chart = alt.Chart(division_salary_totals).mark_bar(color=MEDIUM_GREEN).encode(
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
            MEDIUM_GREEN,
            LIGHT_GREEN
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Memphis Parks</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/local_police: {top_paying_memphis_parks_job}",
                value=f"${max_memphis_parks_salary/1e3:,.1f}k",  
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/assignment: {top_paying_memphis_parks_part_time_job}",
                value=f"${max_memphis_parks_hourly_rate:.0f}/hr",  
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_memphis_parks_salary/1e3:,.1f}k",  
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_memphis_parks_hourly_rate:.0f}/hr",  
                delta=None,
            )

    st.markdown('### Memphis Parks Employment Breakdown')
    
    memphis_parks_row2_cols = st.columns(2, gap="xlarge")

    with memphis_parks_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_memphis_parks_employees,
                total_part_time_memphis_parks_employees,
                total_memphis_parks_employees
            ),
            unsafe_allow_html=True
        )

    with memphis_parks_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_memphis_parks_totals_df,
            MEDIUM_GREEN,
            LIGHT_GREEN
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Library Services</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/local_police: {top_paying_library_services_job}",
                value=f"${max_library_services_salary/1e3:,.1f}k",  
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/assignment: {top_paying_library_services_part_time_job}",
                value=f"${max_library_services_hourly_rate:.0f}/hr",  
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_library_services_salary/1e3:,.1f}k",  
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_library_services_hourly_rate:.0f}/hr",  
                delta=None,
            )

    st.space()

    st.markdown('### Library Services Employment Breakdown')
    
    library_row2_cols = st.columns(2, gap="xlarge")

    with library_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_library_employees,
                total_part_time_library_employees,
                total_library_employees
            ),
            unsafe_allow_html=True
        )

    with library_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_library_totals_df,
            MEDIUM_GREEN,
            LIGHT_GREEN
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Housing and Community Development</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/local_police: {top_paying_housing_community_job}".replace("Hcd", "HCD"),
                value=f"${max_housing_community_salary/1e3:,.1f}k",  
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/assignment: {top_paying_housing_community_part_time_job}".replace("HCD", ""),
                value=f"${max_housing_community_hourly_rate:.0f}/hr",  
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_housing_community_salary/1e3:,.1f}k",  
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_housing_community_hourly_rate:.0f}/hr",  
                delta=None,
            )

    st.space()

    st.markdown('### Housing and Community Development Employment Breakdown')
    
    housing_row2_cols = st.columns(2, gap="xlarge")

    with housing_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_housing_employees,
                total_part_time_housing_employees,
                total_housing_employees
            ),
            unsafe_allow_html=True
        )

    with housing_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_housing_totals_df,
            MEDIUM_GREEN,
            LIGHT_GREEN
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    # st.markdown(
    #     """
    #     **To do:**
    #     - SECTION: Salaries by Division Category / Divisions
    #         - Total Salary of Stronger Neighborhoods Workforce
    #         - Total Salaries by Division
    #         - Employee Workforce
    #             - Total full-time vs part-time employees across division category
    #             - Total employee breakdown by division
    #             - Percent of workforce by division
    #     - ~~SECTION: Memphis Parks~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: Libraries~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: Housing & Community Development~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     """
    # )