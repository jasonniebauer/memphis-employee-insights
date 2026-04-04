import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
from shared.processing import get_division_details
from shared.utilities import employment_type_table, employment_type_pie_chart
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

    /* Override metric delta colors */
    [data-testid="stMetricDelta"] {
        background: #FEEFC3 !important;
        color: #202124 !important;
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

# # Calculate division salary percentage of total
# division_salary_totals['Percentage'] = (
#     division_salary_totals['Annual Salary'] / division_salary_totals['Annual Salary'].sum()
# )

# Get the total salary of Good Government workforce (in millions)
good_government_total_salary = df['Annual Salary'].sum() / 1e6

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
governance_df = df.copy()
# Filter employees to only those in Governance
governance_df = governance_df[governance_df['Category'] == 'Governance']

# Get total number of Governance employees
total_governance_employees = len(governance_df)
# Get total number of full-time employees
total_full_time_governance_employees = (governance_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_governance_employees = (governance_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Governance employees by employment type
employment_type_governance_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_governance_employees / total_governance_employees,
        total_part_time_governance_employees / total_governance_employees
    ],
    "Count": [
        total_full_time_governance_employees,
        total_part_time_governance_employees
    ]
})

# Make a copy of the original DataFrame
finance_df = df.copy()
# Filter employees to only those in Finance
finance_df = finance_df[finance_df['Category'] == 'Finance']

# Get total number of Finance employees
total_finance_employees = len(finance_df)
# Get total number of full-time employees
total_full_time_finance_employees = (finance_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_finance_employees = (finance_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Finance employees by employment type
employment_type_finance_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_finance_employees / total_finance_employees,
        total_part_time_finance_employees / total_finance_employees
    ],
    "Count": [
        total_full_time_finance_employees,
        total_part_time_finance_employees
    ]
})

# Make a copy of the original DataFrame
hr_df = df.copy()
# Filter employees to only those in Human Resources
hr_df = hr_df[hr_df['Category'] == 'HR']

# Get total number of Human Resources employees
total_hr_employees = len(hr_df)
# Get total number of full-time employees
total_full_time_hr_employees = (hr_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_hr_employees = (hr_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Human Resources employees by employment type
employment_type_hr_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_hr_employees / total_hr_employees,
        total_part_time_hr_employees / total_hr_employees
    ],
    "Count": [
        total_full_time_hr_employees,
        total_part_time_hr_employees
    ]
})

# Make a copy of the original DataFrame
it_df = df.copy()
# Filter employees to only those in Information Technology
it_df = it_df[it_df['Category'] == 'IT']

# Get total number of Information Technology employees
total_it_employees = len(it_df)
# Get total number of full-time employees
total_full_time_it_employees = (it_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_it_employees = (it_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Information Technology employees by employment type
employment_type_it_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_it_employees / total_it_employees,
        total_part_time_it_employees / total_it_employees
    ],
    "Count": [
        total_full_time_it_employees,
        total_part_time_it_employees
    ]
})

# Make a copy of the original DataFrame
legal_df = df.copy()
# Filter employees to only those in Legal
legal_df = legal_df[legal_df['Category'] == 'Legal']

# Get total number of Legal employees
total_legal_employees = len(legal_df)
# Get total number of full-time employees
total_full_time_legal_employees = (legal_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_legal_employees = (legal_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Legal employees by employment type
employment_type_legal_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_legal_employees / total_legal_employees,
        total_part_time_legal_employees / total_legal_employees
    ],
    "Count": [
        total_full_time_legal_employees,
        total_part_time_legal_employees
    ]
})

(
    top_paying_governance_job,
    max_governance_salary,
    min_governance_salary,
    top_paying_governance_part_time_job,
    max_governance_hourly_rate,
    min_governance_hourly_rate,
    average_governance_salary,
    average_governance_hourly_rate,
    total_unique_governance_jobs,
    total_governance_employees,
    total_full_time_governance_employees,
    total_part_time_governance_employees,
    employment_type_governance_totals_df
) = get_division_details('Governance')

(
    top_paying_finance_job,
    max_finance_salary,
    min_finance_salary,
    top_paying_finance_part_time_job,
    max_finance_hourly_rate,
    min_finance_hourly_rate,
    average_finance_salary,
    average_finance_hourly_rate,
    total_unique_finance_jobs,
    total_finance_employees,
    total_full_time_finance_employees,
    total_part_time_finance_employees,
    employment_type_finance_totals_df
) = get_division_details('Finance and Administration')

(
    top_paying_legal_job,
    max_legal_salary,
    min_legal_salary,
    top_paying_legal_part_time_job,
    max_legal_hourly_rate,
    min_legal_hourly_rate,
    average_legal_salary,
    average_legal_hourly_rate,
    total_unique_legal_jobs,
    total_legal_employees,
    total_full_time_legal_employees,
    total_part_time_legal_employees,
    employment_type_legal_totals_df
) = get_division_details('Legal')

(
    top_paying_human_resources_job,
    max_human_resources_salary,
    min_human_resources_salary,
    top_paying_human_resources_part_time_job,
    max_human_resources_hourly_rate,
    min_human_resources_hourly_rate,
    average_human_resources_salary,
    average_human_resources_hourly_rate,
    total_unique_human_resources_jobs,
    total_human_resources_employees,
    total_full_time_human_resources_employees,
    total_part_time_human_resources_employees,
    employment_type_human_resources_totals_df
) = get_division_details('Human Resources')

(
    top_paying_info_tech_job,
    max_info_tech_salary,
    min_info_tech_salary,
    top_paying_info_tech_part_time_job,
    max_info_tech_hourly_rate,
    min_info_tech_hourly_rate,
    average_info_tech_salary,
    average_info_tech_hourly_rate,
    total_unique_info_tech_jobs,
    total_info_tech_employees,
    total_full_time_info_tech_employees,
    total_part_time_info_tech_employees,
    employment_type_info_tech_totals_df
) = get_division_details('Information Technology')

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

        st.markdown(
            """
            <div class="table-row">
                <span class="bold">Division</span>
                <span class="bold">Percent of Good Government Salaries</span>
            </div>
            <div class="table-row">
                <span>Governance</span>
                <span>29.4%</span>
            </div>
            <div class="table-row"">
                <span>Finance</span>
                <span>20.9%</span>
            </div>
            <div class="table-row"">
                <span>Legal</span>
                <span>20.6%</span>
            </div>
            <div class="table-row"">
                <span>HR</span>
                <span>14.9%</span>
            </div>
            <div class="table-row"">
                <span>IT</span>
                <span>14.2%</span>
            </div>
            <div class="table-row">
                <span class="bold">Total</span>
                <span class="bold">100%</span>
            </div>
            """, unsafe_allow_html=True
        )

        st.space()

        st.metric(
            label=":material/account_balance: Good Government Workforce Salaries",
            value=f"${good_government_total_salary:,.1f}M",  
            delta=None,
        )

    with salary_cols[1]:
        chart = alt.Chart(division_salary_totals).mark_bar(color=YELLOW).encode(
            x=alt.X(
                'Category',
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
                alt.Tooltip("Category:N", title="Category"),
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
            YELLOW,
            LIGHT_YELLOW
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Governance</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/gavel: {top_paying_governance_job}",
                value=(
                    f"${max_governance_salary/1e3:,.0f}k"
                    if round(max_governance_salary)%1000 == 0
                    else f"${max_governance_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/pets: {top_paying_governance_part_time_job}",
                value=f"${max_governance_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_governance_salary/1e3:,.1f}k",  
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_governance_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### Governance Employment Breakdown')
    
    governance_row2_cols = st.columns(2, gap="xlarge")

    with governance_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_governance_employees,
                total_part_time_governance_employees,
                total_governance_employees
            ),
            unsafe_allow_html=True
        )

    with governance_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_governance_totals_df,
            YELLOW,
            LIGHT_YELLOW
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Finance</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/paid: {top_paying_finance_job}".replace("Financial Officer Chief", "Chief Financial Officer"),
                value=(
                    f"${max_finance_salary/1e3:,.0f}k"
                    if round(max_finance_salary)%1000 == 0
                    else f"${max_finance_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/checkbook: {top_paying_finance_part_time_job}",
                value=f"${max_finance_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_finance_salary/1e3:,.1f}k",  
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_finance_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### Finance Employment Breakdown')
    
    finance_row2_cols = st.columns(2, gap="xlarge")

    with finance_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_finance_employees,
                total_part_time_finance_employees,
                total_finance_employees
            ),
            unsafe_allow_html=True
        )

    with finance_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_finance_totals_df,
            YELLOW,
            LIGHT_YELLOW
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Human Resources</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/person_celebrate: {top_paying_human_resources_job}".replace("Human Resources Officer Chief", "Chief Human Resources Officer"),
                value=(
                    f"${max_human_resources_salary/1e3:,.0f}k"
                    if round(max_human_resources_salary)%1000 == 0
                    else f"${max_human_resources_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/universal_currency: {top_paying_human_resources_part_time_job}".replace("Compensation Coord Sr", "Sr. Compensation Coordinator"),
                value=f"${max_human_resources_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_human_resources_salary/1e3:,.1f}k",  
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_human_resources_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### HR Employment Breakdown')
    
    hr_row2_cols = st.columns(2, gap="xlarge")

    with hr_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_hr_employees,
                total_part_time_hr_employees,
                total_hr_employees
            ),
            unsafe_allow_html=True
        )

    with hr_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_hr_totals_df,
            YELLOW,
            LIGHT_YELLOW
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Information Technology</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/badge: {top_paying_info_tech_job}".replace("Info", "IT"),
                value=(
                    f"${max_info_tech_salary/1e3:,.0f}k"
                    if round(max_info_tech_salary)%1000 == 0
                    else f"${max_info_tech_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/laptop_chromebook: {top_paying_info_tech_part_time_job}".replace("Internship Urban Fellow", "Internship (Urban Fellow)"),
                value=f"${max_info_tech_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_info_tech_salary/1e3:,.1f}k",  
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_info_tech_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### IT Employment Breakdown')
    
    it_row2_cols = st.columns(2, gap="xlarge")

    with it_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_it_employees,
                total_part_time_it_employees,
                total_it_employees
            ),
            unsafe_allow_html=True
        )

    with it_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_it_totals_df,
            YELLOW,
            LIGHT_YELLOW
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Legal</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/balance: {top_paying_legal_job}".replace("Legal Officer Chief", "Chief Legal Officer"),
                value=(
                    f"${max_legal_salary/1e3:,.0f}k"
                    if round(max_legal_salary)%1000 == 0
                    else f"${max_legal_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/fact_check: {top_paying_legal_part_time_job}".replace("Rec", "Records"),
                value=f"${max_legal_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_legal_salary/1e3:,.1f}k",  
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_legal_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### Legal Employment Breakdown')
    
    legal_row2_cols = st.columns(2, gap="xlarge")

    with legal_row2_cols[0]:
        st.markdown("[ PLACEHOLDER FOR SUMMARY ]")

        st.markdown(
            employment_type_table(
                total_full_time_legal_employees,
                total_part_time_legal_employees,
                total_legal_employees
            ),
            unsafe_allow_html=True
        )

    with legal_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_legal_totals_df,
            YELLOW,
            LIGHT_YELLOW
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")
