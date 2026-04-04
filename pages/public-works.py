import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
from shared.processing import get_division_details
from shared.utilities import employment_type_table, employment_type_pie_chart
from shared.colors import BLUE, MEDIUM_BLUE, LIGHT_BLUE


##################################################
# Page initialization and setup
##################################################
st.set_page_config(
    page_title="Memphis Employee Insights – Public Works",
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
    [data-testid="stPageLink-NavLink"][href="public-works"] {
        background: #D2E3FC;
        border-left: 5px solid #4285F4;
        padding-left: 0.2rem;
    }
            
    /* Override metric delta colors */
    [data-testid="stMetricDelta"] {
        background: #D2E3FC !important;
        color: #202124 !important;
    }
</style>
""", unsafe_allow_html=True)

##################################################
# Data Preparation
##################################################

# Get data from session state
df = initialize_data()

# Filter DataFrame to Public Works divisions
df = df[df['Division Category'] == 'Public Works']

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

# Get the total salary for Public Works workforce (in millions)
public_works_total_salary = df['Annual Salary'].sum() / 1e6

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
public_works_df = df.copy()
# Filter employees to only those in Public Works Services
public_works_df = public_works_df[public_works_df['Division Name'] == 'Public Works']

# Get total number of Public Works employees
total_public_works_employees = len(public_works_df)
# Get total number of full-time employees
total_full_time_public_works_employees = (public_works_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_public_works_employees = (public_works_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Public Works employees by employment type
employment_type_public_works_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_public_works_employees / total_public_works_employees,
        total_part_time_public_works_employees / total_public_works_employees
    ],
    "Count": [
        total_full_time_public_works_employees,
        total_part_time_public_works_employees
    ]
})

# Make a copy of the original DataFrame
solid_waste_df = df.copy()
# Filter employees to only those in Solid Waste Management
solid_waste_df = solid_waste_df[solid_waste_df['Division Name'] == 'Solid Waste']

# Get total number of Solid Waste Management employees
total_solid_waste_employees = len(solid_waste_df)
# Get total number of full-time employees
total_full_time_solid_waste_employees = (solid_waste_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_solid_waste_employees = (solid_waste_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing Solid Waste Management employees by employment type
employment_type_solid_waste_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_solid_waste_employees / total_solid_waste_employees,
        total_part_time_solid_waste_employees / total_solid_waste_employees
    ],
    "Count": [
        total_full_time_solid_waste_employees,
        total_part_time_solid_waste_employees
    ]
})

# Make a copy of the original DataFrame
general_services_df = df.copy()
# Filter employees to only those in General Services
general_services_df = general_services_df[general_services_df['Division Name'] == 'General Services']

# Get total number of General Services employees
total_general_services_employees = len(general_services_df)
# Get total number of full-time employees
total_full_time_general_services_employees = (general_services_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_general_services_employees = (general_services_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing General Services employees by employment type
employment_type_general_services_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_general_services_employees / total_general_services_employees,
        total_part_time_general_services_employees / total_general_services_employees
    ],
    "Count": [
        total_full_time_general_services_employees,
        total_part_time_general_services_employees
    ]
})

# Make a copy of the original DataFrame
city_engineering_df = df.copy()
# Filter employees to only those in City Engineering
city_engineering_df = city_engineering_df[city_engineering_df['Division Name'] == 'City Engineering']

# Get total number of City Engineering employees
total_city_engineering_employees = len(city_engineering_df)
# Get total number of full-time employees
total_full_time_city_engineering_employees = (city_engineering_df['Employment Type'] == 'Full-time').sum()
# Get total number of part-time employees
total_part_time_city_engineering_employees = (city_engineering_df['Employment Type'] == 'Part-time').sum()

# Create DataFrame for categorizing City Engineering employees by employment type
employment_type_city_engineering_totals_df = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [
        total_full_time_city_engineering_employees / total_city_engineering_employees,
        total_part_time_city_engineering_employees / total_city_engineering_employees
    ],
    "Count": [
        total_full_time_city_engineering_employees,
        total_part_time_city_engineering_employees
    ]
})
print()
(
    top_paying_public_works_job,
    max_public_works_salary,
    min_public_works_salary,
    top_paying_public_works_part_time_job,
    max_public_works_hourly_rate,
    min_public_works_hourly_rate,
    average_public_works_salary,
    average_public_works_hourly_rate,
    total_unique_public_works_jobs,
    total_public_works_employees,
    total_full_time_public_works_employees,
    total_part_time_public_works_employees,
    employment_type_public_works_totals_df
) = get_division_details('Public Works')

(
    top_paying_solid_waste_job,
    max_solid_waste_salary,
    min_solid_waste_salary,
    top_paying_solid_waste_part_time_job,
    max_solid_waste_hourly_rate,
    min_solid_waste_hourly_rate,
    average_solid_waste_salary,
    average_solid_waste_hourly_rate,
    total_unique_solid_waste_jobs,
    total_solid_waste_employees,
    total_full_time_solid_waste_employees,
    total_part_time_solid_waste_employees,
    employment_type_solid_waste_totals_df
) = get_division_details('Solid Waste')

(
    top_paying_general_services_job,
    max_general_services_salary,
    min_general_services_salary,
    top_paying_general_services_part_time_job,
    max_general_services_hourly_rate,
    min_general_services_hourly_rate,
    average_general_services_salary,
    average_general_services_hourly_rate,
    total_unique_general_services_jobs,
    total_general_services_employees,
    total_full_time_general_services_employees,
    total_part_time_general_services_employees,
    employment_type_general_services_totals_df
) = get_division_details('General Services')

(
    top_paying_city_engineering_job,
    max_city_engineering_salary,
    min_city_engineering_salary,
    top_paying_city_engineering_part_time_job,
    max_city_engineering_hourly_rate,
    min_city_engineering_hourly_rate,
    average_city_engineering_salary,
    average_city_engineering_hourly_rate,
    total_unique_city_engineering_jobs,
    total_city_engineering_employees,
    total_full_time_city_engineering_employees,
    total_part_time_city_engineering_employees,
    employment_type_city_engineering_totals_df
) = get_division_details('City Engineering')

##################################################
# UI Content
##################################################
st.space()

with st.spinner('Loading data and calculations...'):
    st.info(
        'Building Better Transparency: Under Active Development – Check Back for More Soon!',
        icon=":material/build:"
    )
    st.title("Public Works")
    st.markdown('<h3 class="pt-0">Public Works, Solid Waste Management, City Engineering, and General Services</h3>', unsafe_allow_html=True)

    st.space()

    st.markdown('<h2 class="pt-0">Salaries by Division</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.text("Public Works employees are organized into four primary categories: Public Works, Solid Waste, General Services, and City Engineering. These categories together account for more than $93.4 million in total salaries within the city's salaried full-time workforce.")
        st.markdown(
            """
            <div class="table-row">
                <span class="bold">Division</span>
                <span class="bold">Percent of Stronger Neighborhoods Salaries</span>
            </div>
            <div class="table-row">
                <span>Public Works</span>
                <span>43.7%</span>
            </div>
            <div class="table-row"">
                <span>Solid Waste Management</span>
                <span>26.6%</span>
            </div>
            <div class="table-row"">
                <span>General Services</span>
                <span>20.3%</span>
            </div>
            <div class="table-row"">
                <span>City Engineering</span>
                <span>9.4%</span>
            </div>
            <div class="table-row">
                <span class="bold">Total</span>
                <span class="bold">100%</span>
            </div>
            """, unsafe_allow_html=True
        )
        st.space()
        st.metric(
            label=":material/tram: Public Works Workforce Salaries",
            value=f"${public_works_total_salary:,.1f}M",  
            delta=None,
        )

    with salary_cols[1]:
        chart = alt.Chart(division_salary_totals).mark_bar(color=MEDIUM_BLUE).encode(
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
        st.text("Public Works, Solid Waste, General Services, and City Engineering together employ 1,807 individuals across a wide range of roles supporting infrastructure maintenance, waste collection, fleet services, and engineering functions. Salaried full-time employees make up more than 87% of this workforce, while part-time and hourly employees (typically in support or seasonal roles) account for nearly 13%.")
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
            MEDIUM_BLUE,
            LIGHT_BLUE
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Public Works</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.text("Salaries in Memphis Public Works vary widely. Entry-level and support roles, such as Inventory Control Clerk, typically start at approximately $30,000 annually. Compensation increases significantly with career progression and specialized positions, with top earners in supervisory, managerial, and director-level roles exceeding $163,000 per year.")
        st.text("Part-time and hourly support roles generally start around $15 per hour, while specialized or higher-skilled part-time and contract positions can reach up to $18 per hour.")
    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/water_drop: {top_paying_public_works_job}",
                value=(
                    f"${max_public_works_salary/1e3:,.0f}k"
                    if round(max_public_works_salary)%1000 == 0
                    else f"${max_public_works_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/agriculture: {top_paying_public_works_part_time_job}".replace("Oper", "Operator").replace("Crewperson", ""),
                value=f"${max_public_works_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_public_works_salary/1e3:,.1f}k",
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_public_works_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### Public Works Employment Breakdown')
    
    public_works_row2_cols = st.columns(2, gap="xlarge")

    with public_works_row2_cols[0]:
        st.text("Memphis Public Works employs 771 individuals across 140 unique job titles spanning maintenance, operations, engineering support, and administrative roles. Full-time employees make up over 90% of the core workforce, while part-time and hourly employees account for nearly 10%. These employees maintain critical city infrastructure, including streets, bridges, drainage systems, sanitation facilities, and traffic control systems.")
        st.markdown(
            employment_type_table(
                total_full_time_public_works_employees,
                total_part_time_public_works_employees,
                total_public_works_employees
            ),
            unsafe_allow_html=True
        )

    with public_works_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_public_works_totals_df,
            MEDIUM_BLUE,
            LIGHT_BLUE
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Solid Waste Management</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.text("Salaries across Solid Waste Management show a broad range. Entry-level positions, such as Office Support Clerk, typically begin around $35,000 per year. With career advancement and specialized skills, pay scales upward, reaching over $145,000 annually for those in supervisory, managerial, and director-level roles.")
        st.text("Part-time and hourly roles generally pay around $15 per hour, with little variation even for more specialized or contract positions.")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/delete: {top_paying_solid_waste_job}",
                value=(
                    f"${max_solid_waste_salary/1e3:,.0f}k"
                    if round(max_solid_waste_salary)%1000 == 0
                    else f"${max_solid_waste_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/mop: {top_paying_solid_waste_part_time_job}",
                value=f"${max_solid_waste_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_solid_waste_salary/1e3:,.1f}k",
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_solid_waste_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### Solid Waste Management Employment Breakdown')
    
    solid_waste_row2_cols = st.columns(2, gap="xlarge")

    with solid_waste_row2_cols[0]:
        st.text("Solid Waste Management employs 575 individuals across 39 unique job titles, spanning sanitation operations, equipment maintenance, driver positions, and administrative support roles. Full-time employees make up over 80% of the core workforce, while part-time and hourly employees account for nearly 20%.")
        st.markdown(
            employment_type_table(
                total_full_time_solid_waste_employees,
                total_part_time_solid_waste_employees,
                total_solid_waste_employees
            ),
            unsafe_allow_html=True
        )

    with solid_waste_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_solid_waste_totals_df,
            MEDIUM_BLUE,
            LIGHT_BLUE
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">General Services</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.text("Salaries across General Services show a broad range. This department is responsible for providing exemplary customer service and Diversified Maintenance Services. Entry-level positions, such as maintenance distribution technician, typically start around $39,000 per year. Pay scales upward with career advancement and specialized skills, reaching over $145,000 annually for supervisory, managerial, and director-level roles.")
        st.text("Part-time and hourly roles generally start at $17 per hour, with more specialized or contract positions increasing to $26 per hour.")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/note_alt: {top_paying_general_services_job}".replace("Svcs", "Services"),
                value=(
                    f"${max_general_services_salary/1e3:,.0f}k"
                    if round(max_general_services_salary)%1000 == 0
                    else f"${max_general_services_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/format_paint: {top_paying_general_services_part_time_job}",
                value=f"${max_general_services_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_general_services_salary/1e3:,.1f}k",
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_general_services_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### General Services Employment Breakdown')
    
    general_services_row2_cols = st.columns(2, gap="xlarge")

    with general_services_row2_cols[0]:
        st.text("General Services employs more than 314 individuals across 70 unique job titles, spanning facility maintenance, fleet maintenance, grounds maintenance, and administrative support roles. Full-time employees make up over 90% of the core workforce, while part-time and hourly employees account for nearly 10%.")
        st.markdown(
            employment_type_table(
                total_full_time_general_services_employees,
                total_part_time_general_services_employees,
                total_general_services_employees
            ),
            unsafe_allow_html=True
        )

    with general_services_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_general_services_totals_df,
            MEDIUM_BLUE,
            LIGHT_BLUE
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">City Engineering</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.text("City Engineering offers a wide salary range across its roles. The department handles engineering design, project management, infrastructure planning, and technical support for the city's capital projects and public works initiatives. Entry-level positions like Painter Apprentice typically start around $32,000 per year, while experienced professionals in supervisory, managerial, and director-level roles can earn more than $145,000 annually.")
        st.text("Part-time and hourly positions generally begin at $15 per hour and can reach up to $21 per hour for specialized or contract work.")

    with salary_cols[1]:
        with st.container(horizontal=True):
            st.metric(
                label=f":material/engineering: {top_paying_city_engineering_job}",
                value=(
                    f"${max_city_engineering_salary/1e3:,.0f}k"
                    if round(max_city_engineering_salary)%1000 == 0
                    else f"${max_city_engineering_salary/1e3:,.1f}k"
                ),
                delta="Top Full-Time Salary",
            )
            st.metric(
                label=f":material/electric_bolt: {top_paying_city_engineering_part_time_job}",
                value=f"${max_city_engineering_hourly_rate:.0f}/hr",
                delta="Top Part-Time Rate",
            )
        st.space()
        with st.container(horizontal=True):
            st.metric(
                label=f"Average full-time salary",
                value=f"${average_city_engineering_salary/1e3:,.1f}k",
                delta=None,
            )
            st.metric(
                label=f"Average part-time rate ",
                value=f"${average_city_engineering_hourly_rate:.0f}/hr",
                delta=None,
            )

    st.space()

    st.markdown('### City Engineering Employment Breakdown')
    
    city_engineering_row2_cols = st.columns(2, gap="xlarge")

    with city_engineering_row2_cols[0]:
        st.text("City Engineering maintains a workforce of more than 147 individuals working across 52 unique job titles. These roles cover a variety of technical and professional positions in engineering design, project management, and infrastructure support. Full-time staff comprise over 91% of the department, with part-time and hourly employees making up the remaining 9%.")

        st.markdown(
            employment_type_table(
                total_full_time_city_engineering_employees,
                total_part_time_city_engineering_employees,
                total_city_engineering_employees
            ),
            unsafe_allow_html=True
        )

    with city_engineering_row2_cols[1]:
        pie_chart_employment_type = employment_type_pie_chart(
            employment_type_city_engineering_totals_df,
            MEDIUM_BLUE,
            LIGHT_BLUE
        )

        st.altair_chart(pie_chart_employment_type, width="stretch")

    # st.markdown(
    #     """
    #     **To do:**
    #     - SECTION: Salaries by Division Category / Divisions
    #         - Total Salary of Public Works Workforce
    #         - Total Salaries by Division
    #         - Employee Workforce
    #             - Total full-time vs part-time employees across division category
    #             - Total employee breakdown by division
    #             - Percent of workforce by division
    #     - ~~SECTION: Public Works~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: Solid Waste Management~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: General Services~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     - ~~SECTION: City Engineering~~
    #         - Employee Workforce
    #             - Total full-time vs part-time employees
    #         - Unique roles + average salary for role
    #         - Top paying position
    #         - Average salary across division
    #         - Average hourly rate across division (if applicable)
    #     """
    # )