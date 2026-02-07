import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data, get_department_summary
from shared.colors import TEAL, LIGHT_TEAL, MEDIUM_RED, MEDIUM_BLUE, MEDIUM_GREEN, YELLOW, LIGHT_GREY, GREY, BLACK


##################################################
# Page initialization and setup
##################################################

st.set_page_config(
    page_title="Memphis Employee Insights",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render navigation sidebar
render_navigation()

# Render reusable styles
render_reusable_styles()

# Load data
df = initialize_data()

# # Load data (cached)
# if 'salary_data' not in st.session_state:
#     st.session_state.salary_data = load_salary_data()

# Page-specific CSS (only runs here on page)
st.markdown(
    """
    <style>
    /* Set background color for active page link */
    [data-testid="stPageLink-NavLink"][href=""] {
        background-color: #DAE2E5 !important;
    }

    /* Set background color for active page link */
    [data-testid="stPageLink-NavLink"][href=""],
    [data-testid="stPageLink-NavLink"][href=""]:hover {
        background: transparent;
        border-left: 5px solid #0097A7;
        padding-left: 0.2rem;
    }

    [data-testid="stMetricDelta"] {
        background: #80DEEA !important;
        color: #202124 !important;
    }

    /* Override Badge colors */
    span.stMarkdownBadge {
        background-color: #80DEEA !important;
        color: #202124 !important;
    }
    </style>
    """, unsafe_allow_html=True)

##################################################
# Data Preparation
##################################################

#
total_divisions = df['Division Name'].nunique()

# 
total_city_salaries = df['Annual Salary'].sum()
total_city_salaries_formatted = total_city_salaries / 1e6

#
total_city_employees = len(df)
# Get total number of unique job titles
total_city_job_titles = df['Job Title'].nunique()

#
average_city_salary = df['Annual Salary'].mean()
# Get total number of salaried employees
total_salaried_employees = (df['Employment Type'] == 'Full-time').sum()
#
total_salaried_job_titles = df[df['Employment Type'] == 'Full-time']['Job Title'].nunique()

#
average_city_hourly_pay = df['Hourly/Per Event Rate'].mean()
# Get total number of part-time employees
total_part_time_employees = (df['Employment Type'] == 'Part-time').sum()
#
total_hourly_job_titles = df[df['Employment Type'] == 'Part-time']['Job Title'].nunique()

#
percent_salaried_employees = total_salaried_employees / total_city_employees
percent_part_time_employees = total_part_time_employees / total_city_employees

# Calculating the sum of all Salaries in each Division Category
division_category_salary_totals = pd.DataFrame(df.groupby('Division Category')['Annual Salary'].sum()).reset_index()

# Sort Division Categories by the sum of all Salaries in descending order
division_category_salary_totals.sort_values(by='Annual Salary', ascending=False, inplace=True)

def custom_logic(row):
    return (row['Annual Salary'] / total_city_salaries) 

# Apply the function to each row (axis=1)
division_category_salary_totals['Percentage'] = division_category_salary_totals.apply(custom_logic, axis=1)

#
public_safety_salary = division_category_salary_totals.loc[
    division_category_salary_totals['Division Category'] == 'Public Safety', 'Annual Salary'
].values[0] / 1e6

#
public_works_salary = division_category_salary_totals.loc[
    division_category_salary_totals['Division Category'] == 'Public Works', 'Annual Salary'
].values[0] / 1e6

#
stronger_neighborhoods_salary = division_category_salary_totals.loc[
    division_category_salary_totals['Division Category'] == 'Stronger Neighborhoods', 'Annual Salary'
].values[0] / 1e6

#
good_government_salary = division_category_salary_totals.loc[
    division_category_salary_totals['Division Category'] == 'Good Government', 'Annual Salary'
].values[0] / 1e6

# Calculating the sum of all Salaries in each Division
division_salary_totals = pd.DataFrame(df.groupby('Division Name')['Annual Salary'].sum()).reset_index()

# Sort Divisions by the sum of all Salaries in descending order
division_salary_totals.sort_values(by='Annual Salary', ascending=False, inplace=True)

#
source = pd.DataFrame({
    "Employment Type": ["Full-time", "Part-time"],
    "Value": [percent_salaried_employees, percent_part_time_employees],
    "Count": [total_salaried_employees, total_part_time_employees]
})

# REUSABLE SNIPPET - utils.py
division_category = 'Public Safety'  # Adjust based on page
public_safety_employees = df.groupby('Division Category').size()[division_category]

# Get division category employee percentage of total city employees
public_safety_employee_percentage = (public_safety_employees / total_city_employees) * 100

public_safety_employee_count = len(df.loc[
    df['Division Category'] == 'Public Safety'
])

public_safety_employee_percentage = (
    public_safety_employee_count / total_city_employees
)

public_works_employee_count = len(df.loc[
    df['Division Category'] == 'Public Works'
])

public_works_employee_percentage = (
    public_works_employee_count / total_city_employees
)

stronger_neighborhoods_employee_count = len(df.loc[
    df['Division Category'] == 'Stronger Neighborhoods'
])

stronger_neighborhoods_employee_percentage = (
    stronger_neighborhoods_employee_count / total_city_employees
)

good_government_employee_count = len(df.loc[
    df['Division Category'] == 'Good Government'
])

good_government_employee_percentage = (
    good_government_employee_count / total_city_employees
)

df_division_category_employee = pd.DataFrame({
    "Division Category": ["Public Safety", "Public Works", "Stronger Neighborhoods", "Good Government"],
    "Value": [public_safety_employee_percentage, public_works_employee_percentage, stronger_neighborhoods_employee_percentage, good_government_employee_percentage],
    "Employees": [public_safety_employee_count, public_works_employee_count, stronger_neighborhoods_employee_count, good_government_employee_count]
})

counts_df = df.groupby('Division Category').size().reset_index(name='Total Employees').sort_values(by='Total Employees', ascending=False)

# Get count of full-time employees for Public Safety
public_safety_full_time_employee_count = len(df.loc[
    (df['Division Category'] == 'Public Safety') & (df['Employment Type'] == 'Full-time')
])

# Get Public Safety full-time employee percentage of total full-time employees 
public_safety_full_time_employee_percentage = (
    public_safety_full_time_employee_count / total_salaried_employees
) * 100

# Get count of full-time employees for Stronger Neighborhoods
stronger_neighborhoods_part_time_employee_count = len(df.loc[
    (df['Division Category'] == 'Stronger Neighborhoods') & (df['Employment Type'] == 'Part-time')
])

# Get Stronger Neighborhoods pull-time employee percentage of total full-time employees 
stronger_neighborhoods_part_time_employee_percentage = (
    stronger_neighborhoods_part_time_employee_count / total_part_time_employees
) * 100

#
employment_type_by_division_category = (
    df['Employment Type']
    .groupby(df['Division Category'])
    .value_counts()
    .reset_index(name='Count')
    .sort_values(by='Count', ascending=False)
)

# RESUSABLE SNIPPET - utils.py
division = 'Police Services'  # Adjust based on page
police_services_employees = df.groupby('Division Name').size()[division]

# Get division employee percentage of total city employees
divison_employee_percentage = (police_services_employees / total_city_employees) * 100

# Get count of full-time employees for Police Services
police_services_full_time_employee_count = len(df.loc[
        (df['Division Name'] == 'Police Services') & (df['Employment Type'] == 'Full-time')
])

# Get Police Services Full-time employee percentage of total full-time employees 
police_services_full_time_employee_percentage = (
    police_services_full_time_employee_count / total_salaried_employees
) * 100

result = (
    df['Employment Type']
    .groupby(df['Division Name'])
    .value_counts()
    .reset_index(name='Count')
)

#
employees_by_division = df.groupby('Division Name').size().reset_index(name="Count").sort_values(by='Count', ascending=False)

##################################################
# UI Content
##################################################

st.space()
with st.spinner('Loading data and calculations...'):
    st.info(
        'Building Better Transparency: Under Active Development – Check Back for More Soon!',
        icon=":material/build:"
    )
    st.title("City of Memphis Employee Insights")
    st.caption("Payroll Snapshot - January 28, 2025")

    """
    This site provides an interactive analysis of employee salaries for the City of Memphis, Tennessee. All data is sourced directly from publicly available records published by the City of Memphis and can be accessed via their official website.

    The dataset includes 8,202 city employees and contains the following key details for each:
    - Job title
    - Division
    - Employment type (full-time or part-time)
    - Annual salary or hourly rate

    The goal is to offer clear, transparent insights into salary distribution, departmental staffing, and compensation patterns across the city's workforce.
    """

    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Salaries by Division Category</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        st.markdown(
            """
            City of Memphis employees are organized into four primary categories: Public Safety, Public Works, Stronger Neighborhoods, and Good Government. Each category groups related divisions that deliver similar public services, operations, or administrative functions under shared leadership to support the community efficiently.
            
            Public Safety accounts for more than 66% of the total salaries across the city's salaried/full-time workforce. This dominant share reflects the high personnel demands of law enforcement, fire services, and emergency response, including shift-based staffing and overtime.
            """
        )
        st.markdown("<p style='font-weight: 600;margin-top:1rem;margin-bottom:0.25rem;line-height:1.0;'>Total Salaries of Memphis Workforce</p>", unsafe_allow_html=True)
        st.markdown(f'<p class="xl-metric left">${total_city_salaries_formatted:,.1f}M<span style="font-size:18px;vertical-align:top;margin-left:0.2rem;">*</span></p>', unsafe_allow_html=True)
        st.caption("<small class='center' style='margin-top:0;line-height:1.0;'>* Does not include part-time, hourly payroll</small>", unsafe_allow_html=True)

    st.space()

    with salary_cols[1]:
        # Define colors
        color_map = {
            "Public Safety": MEDIUM_RED,
            "Public Works": MEDIUM_BLUE,
            "Stronger Neighborhoods": MEDIUM_GREEN,
            "Good Government": YELLOW,
        }
        
        salary_distribution_by_division_category = alt.Chart(division_category_salary_totals).mark_arc().encode(
            theta=alt.Theta("Percentage:Q", stack=True),
            color=alt.Color(
                "Division Category:N",
                title="Category",
                scale=alt.Scale(
                    domain=list(color_map.keys()),
                    range=list(color_map.values())
                )
            ),
            tooltip=[
                alt.Tooltip("Division Category:N", title="Category"),
                alt.Tooltip("Annual Salary:Q", format="$,.2f", title="Total Salary"),
                alt.Tooltip("Percentage:Q", format=".1%", title="Percentage")
            ]
        ).properties(
            title='Total Salaries by Division Category'
        )

        st.altair_chart(salary_distribution_by_division_category, width="stretch")
        
    st.space()

    with st.container():
        division_category_cols = st.columns(4)

        with division_category_cols[0]:
            st.markdown(f'<p class="xl-metric red">${public_safety_salary:,.1f}M</p>', unsafe_allow_html=True)
            st.markdown('<p class="center bold">Public Safety</p>', unsafe_allow_html=True)

        with division_category_cols[1]:
            st.markdown(f'<p class="xl-metric blue">${public_works_salary:,.1f}M</p>', unsafe_allow_html=True)
            st.markdown('<p class="center bold">Public Works</p>', unsafe_allow_html=True)

        with division_category_cols[2]:
            st.markdown(f'<p class="xl-metric green">${stronger_neighborhoods_salary:,.1f}M</p>', unsafe_allow_html=True)
            st.markdown('<p class="center bold">Stronger Neighborhoods</p>', unsafe_allow_html=True)

        with division_category_cols[3]:
            st.markdown(f'<p class="xl-metric yellow">${good_government_salary:,.1f}M</p>', unsafe_allow_html=True)
            st.markdown('<p class="center bold">Good Government</p>', unsafe_allow_html=True)

    st.space()
    st.space()

    with st.container():
        # Define colors
        division_color_scale = alt.Scale(
            domain=[
                "Police Services",
                "Fire Services",
                "Public Works",
                "Solid Waste",
                "General Services",
                "Memphis Parks",
                "Library Services",
                "City Engineering",
                "Executive",
                "Finance and Administration",
                "Human Resources",
                "Information Technology",
                "City Attorney",
                "Housing and Community Development",
                "City Court Clerk",
                "Legislative",
                "Judicial",
            ],
            range=[
                MEDIUM_RED,
                MEDIUM_RED,
                MEDIUM_BLUE,
                MEDIUM_BLUE,
                MEDIUM_BLUE,
                MEDIUM_GREEN,
                MEDIUM_GREEN,
                MEDIUM_BLUE,
                YELLOW,
                YELLOW,
                YELLOW,
                YELLOW,
                YELLOW,
                MEDIUM_GREEN,
                YELLOW,
                YELLOW,
                YELLOW,
            ]
        )

        chart = alt.Chart(division_salary_totals).mark_bar().encode(
            x=alt.X('Annual Salary', axis=alt.Axis(title='Annual Salary Total', format='$,s')),
            y=alt.Y(
                'Division Name',
                sort=None,
                axis=alt.Axis(title=None, labelLimit=300)
            ),
            color=alt.Color("Division Name:N", scale=division_color_scale, legend=None),
            tooltip=[
                alt.Tooltip('Division Name'),
                alt.Tooltip('Annual Salary', format="$,.2f")
            ]
        ).properties(
            title=alt.TitleParams(
                text='Total Salaries by Division',
                subtitle=['Fiscal Year 2025 | Source: City of Memphis'],
                anchor='start'
            )
        )

        st.altair_chart(chart, width="stretch")

    #--------------------------------------------------------
    st.space()
    st.divider()
    st.space()

    st.markdown('<h2 class="pt-0">Employee Workforce Overview</h2>', unsafe_allow_html=True)
    st.markdown('### Employment Breakdown')

    overview_col_1, overview_col_2 = st.columns(2, gap="xlarge")

    with overview_col_1:
        st.markdown(
            f"""
            The City of Memphis employs 8,202 individuals across {total_divisions} divisions supporting essential public services throughout the city. Salaried employees account for over 83% of the City's core full-time workforce, while part-time, hourly employees (typically in seasonal, support, or entry-level roles) make up nearly 17%.

            <div class="table-row">
                <span class="bold">Full-time (salaried) employees</span>
                <span>{total_salaried_employees:,}</span>
            </div>
            <div class="table-row"">
                <span class="bold">Part-time employees</span>
                <span>{total_part_time_employees:,}</span>
            </div>
            <div class="table-row">
                <span class="bold">Total employees</span>
                <span>{total_city_employees:,}</span>
            </div>
            """, unsafe_allow_html=True
        )
        # st.markdown(
        #     f"""
        #     <div class="table-row"">
        #         <span class="bold">Average annual salary (full-time employees)</span>
        #         <span>${average_city_salary:,.2f}</span>
        #     </div>
        #     <div class="table-row" style="margin-bottom:2rem;">
        #         <span class="bold">Average hourly rate (part-time employees)</span>
        #         <span>${average_city_hourly_pay:.2f}</span>
        #     </div>
        #     """, unsafe_allow_html=True
        # )

    with overview_col_2:
        # Define colors
        employee_classification_color_map = {
            "Full-time": TEAL,
            "Part-time": LIGHT_TEAL
        }

        pie_chart_job_category = alt.Chart(source).mark_arc().encode(
            theta="Value",
            color=alt.Color("Employment Type", scale=alt.Scale(
                domain=list(employee_classification_color_map.keys()),
                range=list(employee_classification_color_map.values())
            )),
            tooltip=[
                "Employment Type",
                alt.Tooltip("Count:Q", format=",", title="Employees"),
                alt.Tooltip("Value:Q", format=".1%", title="Percentage")
            ]
        )
        # .properties(
        #     title='Employees by Employment Type'
        # )

        st.altair_chart(pie_chart_job_category, width="stretch")

    st.space()

    st.markdown('### Employees by Division Category')

    employees_by_division_category_cols = st.columns(2, gap="xlarge")

    with employees_by_division_category_cols[0]:
        st.badge(
            "Public Safety Dominates the Memphis Workforce",
            icon=":material/local_police:"
        )
        
        st.markdown(
            """
            Public Safety (including Police, Fire, and related services) accounts for more than 54% of all City of Memphis employees, making it by far the largest workforce category. This reflects the city's significant investment in law enforcement, emergency response, and public protection. These areas often require higher headcounts due to 24/7 operations and shift-based staffing.
            """
        )

        st.space()

        employees_by_division_category_summary_cols = st.columns(2)

        with employees_by_division_category_summary_cols[0]:
            st.metric(
                label=":material/local_police: Public Safety Employees",
                value="4,466",  
                delta=None,
            )
        with employees_by_division_category_summary_cols[1]:
            st.metric(
                label="Public Safety :material/percent: of City Employees",
                value=f"{public_safety_employee_percentage*100:.1f}%",
                delta=None,
            )

    with employees_by_division_category_cols[1]:
        chart = alt.Chart(counts_df).mark_bar(color=TEAL).encode(
            x=alt.X(
                'Division Category',
                axis=alt.Axis(labelAngle=0),  # Rotate labels
                sort=None,
                title=None,
            ),
            y=alt.Y(
                'Total Employees',
                axis=alt.Axis(format=',d'),  # Format numbers with comma 
            ),
            tooltip=[
                alt.Tooltip("Division Category:N", title="Category"),
                alt.Tooltip("Total Employees:Q", format=",d", title="Employees")
            ]
        )
        st.altair_chart(chart)

    st.space()

    st.markdown('### Employment Type by Division Category')

    employment_type_by_division_category_cols = st.columns(2, gap="xlarge")

    with employment_type_by_division_category_cols[0]:
        st.markdown(
            """
            Public Safety leads full-time (salaried) roles, accounting for more than 61% of all salaried City of Memphis employees. In contrast, Stronger Neighborhoods represents nearly 50% of part-time positions, likely due to seasonal, event-based, or community-focused roles (e.g. lifeguards, park staff, or temporary neighborhood services).

            This split underscores different staffing needs: Public Safety relies heavily on stable, round-the-clock full-time positions (e.g. officers and firefighters), while other divisions like Stronger Neighborhoods lean on flexible part-time labor.
            """
        )
    with employment_type_by_division_category_cols[1]:
        st.metric(
            label=":material/local_police: Public Safety",
            value=f"{public_safety_full_time_employee_percentage:.1f}%",
            delta="Largest Full-time Division Category"
        )

        st.space()

        st.metric(
            label=':material/psychiatry: Stronger Neighborhoods',
            value=f"{stronger_neighborhoods_part_time_employee_percentage:.1f}%",
            delta="Largest Part-time Division Category"
        )

    st.space()

    employment_type_by_division_category_chart = alt.Chart(employment_type_by_division_category).mark_bar().encode(
        x=alt.X(
            'Division Category:N',
            axis=alt.Axis(labelAngle=0),  # Rotate labels
            sort=None,
            title=None,
        ),
        y=alt.Y(
            'sum(Count):Q',
            axis=alt.Axis(
                format=',d',
                title='Total Employees',
            ),
            
        ),
        # Sort the segments within each bar by the 'Employment Type' field in descending order
        order=alt.Order('Employment Type', sort='ascending'),
        color=alt.Color('Employment Type:N',
            title='Employment Type',
            scale=alt.Scale(
                domain=['Full-time', 'Part-time'],
                range=[TEAL, LIGHT_TEAL]
                
            ),
        ),
        tooltip=[
            alt.Tooltip('Division Category:N', title='Category'),
            alt.Tooltip('Employment Type:N', title='Employment Type'),
            alt.Tooltip('sum(Count):Q', title='Employees', format=',d')
        ]
    ).properties(
        title=alt.TitleParams(
            text='Employment Type Breakdown: Full-Time vs. Part-Time by Division Category',
            subtitle=['Fiscal Year 2025 | Source: City of Memphis'],
            anchor='start'
        )
    )

    st.altair_chart(employment_type_by_division_category_chart, width="stretch")

    st.space()

    st.markdown('### Employees by Division')

    new_cols = st.columns(2, gap="xlarge")

    with new_cols[0]:
        st.badge(
            "Police and Fire Lead City Workforce Headcount",
            icon=":material/local_police:"
        )

        st.markdown(
            """
            More than 1/3 (over 33%) of all City of Memphis employees work in Police Services, the single largest division by headcount. Fire Services follows closely, representing more than 1/5 (over 20%) of the total workforce. Together, these two core public safety functions account for a majority of city staffing, reflecting the priority on law enforcement, emergency response, and round-the-clock protection needs.
            """
        )

        employees_by_division_chart = alt.Chart(employees_by_division).mark_bar(color=TEAL).encode(
            x=alt.X(
                'Count',
                title='Total Employees'
            ),
            y=alt.Y(
                'Division Name',
                sort=None,
                axis=alt.Axis(title=None, labelLimit=300)
            ),
            tooltip=[
                alt.Tooltip('Division Name:N', title='Division'),
                alt.Tooltip('Count:Q', title='Total Employees', format=',d')
            ]
        ).properties(
            title=alt.TitleParams(
                text='Employees by Division',
                subtitle=['Fiscal Year 2025 | Source: City of Memphis'],
                anchor='start'
            )
        )

        st.altair_chart(
            employees_by_division_chart,
            width='stretch'
        )

    with new_cols[1]:
        st.markdown(
            f"""
            <div class="table-row">
                <span class="bold">Division</span>
                <span class="bold">Percent of Memphis Workforce</span>
            </div>
            <div class="table-row">
                <span>Police Services</span>
                <span>33.1%</span>
            </div>
            <div class="table-row"">
                <span>Fire Services</span>
                <span>21.3%</span>
            </div>
            <div class="table-row">
                <span>Memphis Parks</span>
                <span>10.6%</span>
            </div>
            <div class="table-row">
                <span>Public Works</span>
                <span>9.4%</span>
            </div>
            <div class="table-row">
                <span>Solid Waste</span>
                <span>7.0%</span>
            </div>
            <div class="table-row">
                <span>General Services</span>
                <span>3.8%</span>
            </div>
            <div class="table-row">
                <span>Library Services</span>
                <span>3.8%</span>
            </div>
            <div class="table-row">
                <span>Executive</span>
                <span>2.7%</span>
            </div>
            <div class="table-row">
                <span>City Engineering</span>
                <span>1.8%</span>
            </div>
            <div class="table-row">
                <span>Human Resource</span>
                <span>1.5%</span>
            </div>
            <div class="table-row">
                <span>Finance and Administration</span>
                <span>1.4%</span>
            </div>
            <div class="table-row">
                <span>Housing and Community Development</span>
                <span>0.8%</span>
            </div>
            <div class="table-row">
                <span>Information Technology</span>
                <span>0.8%</span>
            </div>
            <div class="table-row">
                <span>City Court Clerk</span>
                <span>0.8%</span>
            </div>
            <div class="table-row">
                <span>City Attorney</span>
                <span>0.7%</span>
            </div>
            <div class="table-row">
                <span>Legislative</span>
                <span>0.4%</span>
            </div>
            <div class="table-row">
                <span>Judicial</span>
                <span>0.1%</span>
            </div>
            <div class="table-row">
                <span class="bold">Total</span>
                <span class="bold">100%</span>
            </div>
            """, unsafe_allow_html=True
        )

    st.space()

    # employees_by_division_chart = alt.Chart(employees_by_division).mark_bar(color=TEAL).encode(
    #     x=alt.X(
    #         'Count',
    #         title='Total Employees'
    #     ),
    #     y=alt.Y(
    #         'Division Name',
    #         sort=None,
    #         axis=alt.Axis(title=None, labelLimit=300)
    #     ),
    #     tooltip=[
    #         alt.Tooltip('Division Name:N', title='Division'),
    #         alt.Tooltip('Count:Q', title='Total Employees', format=',d')
    #     ]
    # ).properties(
    #     title=alt.TitleParams(
    #         text='Employees by Division',
    #         subtitle=['Fiscal Year 2025 | Source: City of Memphis'],
    #         anchor='start'
    #     )
    # )

    # st.altair_chart(
    #     employees_by_division_chart,
    #     use_container_width=True
    # )

    st.space()

    st.markdown('### Employment Type by Division')

    employement_division_cols = st.columns(2, gap="xlarge")

    with employement_division_cols[0]:
        st.markdown(
            """
            Police Services leads the full-time workforce, accounting for nearly 36% of all salaried City of Memphis employees. This reflects the need for stable staff in law enforcement roles. In contrast, Memphis Parks dominates the part-time/hourly workforce, representing more than 46% of all part-time employees. Seasonal or flexible roles (such as lifeguards, park attendants, recreation staff, and event support) likely drive this concentration.

            Notably, three divisions have zero part-time or hourly employees: City Attorney, Legislative, and Judicial. These functions typically rely exclusively on full-time, salaried positions.
            """
        )

    with employement_division_cols[1]:
        st.metric(
            label=f":material/local_police: Police Services",
            # value=f"{divison_employee_percentage:.1f}%",
            value=f"{police_services_full_time_employee_percentage:.1f}%",
            delta="Largest Full-time Division"
        )

        st.space()

        st.metric(
            label=":material/park: Memphis Parks",
            value="46.2%",
            delta="Largest Part-time Division"
        )

    st.space()
    # st.space()

    chart = alt.Chart(result).mark_bar().encode(
        x=alt.X('sum(Count):Q',
            axis=alt.Axis(format=',d', title='Number of Employees')
        ),
        y=alt.Y('Division Name:N',
            sort=alt.EncodingSortField(
                field='Count',
                op='sum',
                order='descending'
            ),
            axis=alt.Axis(title=None, labelLimit=300)
        ),
        color=alt.Color('Employment Type:N',
            title='Employment Type',
            scale=alt.Scale(
                domain=['Full-time', 'Part-time'],
                range=[TEAL, LIGHT_TEAL]
                
            )),
        tooltip=[
            alt.Tooltip('Division Name:N', title='Division'),
            alt.Tooltip('Employment Type:N', title='Employment Type'),
            alt.Tooltip('sum(Count):Q', title='Count', format=',d')
        ]
    ).properties(
        title=alt.TitleParams(
            text='Employment Type Breakdown: Full-Time vs. Part-Time by Division',
            subtitle=['Fiscal Year 2025 | Source: City of Memphis'],
            anchor='start'
        )
    )

    st.altair_chart(chart, width="stretch")