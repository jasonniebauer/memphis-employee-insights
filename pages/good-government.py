import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
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
        st.markdown("[ PLACEHOLDER FOR CHART]")

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
        st.markdown("[ PLACEHOLDER FOR CHART]")

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
        st.markdown("[ PLACEHOLDER FOR CHART]")

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
        st.markdown("[ PLACEHOLDER FOR CHART]")

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
        st.markdown("[ PLACEHOLDER FOR CHART]")

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