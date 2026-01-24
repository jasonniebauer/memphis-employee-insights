import streamlit as st
import altair as alt
import pandas as pd
from shared.navigation import render_navigation
from shared.data_loader import initialize_data, get_department_summary
from shared.colors import RED, BLUE, GREEN, YELLOW, LIGHT_GREY, GREY, BLACK
from config import PAGE_CONFIG


st.set_page_config(**PAGE_CONFIG)

# Render navigation sidebar
render_navigation()

# Load data
df = initialize_data()

# # Load data (cached)
# if 'salary_data' not in st.session_state:
#     st.session_state.salary_data = load_salary_data()

# Page-specific CSS (only runs here n page)
st.markdown(
    """
    <style>
    /* Hide GitHub buttons on public site */
    [data-testid="stToolbarActionButton"] {
        display: none !important;
    }

    /* Remove padding from top of page */
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}

    /* Remove white background from header section */
    header { background: transparent !important; }

    /* Set background color for active page link */
    [data-testid="stPageLink-NavLink"][href=""] {
        background-color: #DAE2E5 !important;
    }

    /* Set background color for active page link */
    [data-testid="stPageLink-NavLink"][href=""],
    [data-testid="stPageLink-NavLink"][href=""]:hover {
        background: transparent;
        border-left: 5px solid #9AA0A6;
        padding-left: 0.2rem;
    }

    .xl-metric {
        font-weight: 600;
        line-height: 1.0;
        font-size: 2.75rem !important;
        margin-bottom: 0;
        text-align: center; 
    }

    [data-testid="stCaptionContainer"] .small-label {
        font-size: smaller !important;
        margin-top: 0;
        line-height: 1.0;
    }

    .center {
        text-align: center;        
    }
    .left {
        text-align: left;        
    }
            
    .bold {
        font-weight: 600;        
    }

    .mb-0 {
        margin-bottom: 0 !important;        
    }
    .pt-0 {
        padding-top: 0 !important;        
    }
            
    .red {
        color: #EA4335;        
    }
    .blue {
        color: #4285F4;        
    }
    .green {
        color: #34A853;        
    }
    .yellow {
        color: #FBBC04;        
    }
    .grey {
        color: #9AA0A6;
    }

    .table-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        border-bottom: 1px solid #F1F3F4;
        padding: 0.2rem 0;
    }
    .table-row:last-of-type {
        border-bottom: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Main content
st.title("City of Memphis Employee Salaries")
# st.markdown("### Overview Dashboard")
st.caption("Payroll Snapshot - January 28, 2025")

"""
This site provides an interactive analysis of employee salaries for the City of Memphis, Tennessee. All data is sourced directly from publicly available records published by the City of Memphis and can be accessed via their official website.

The dataset includes 8,202 city employees and contains the following key details for each:
- Job title
- Division
- Employment type (regular or part-time)
- Annual salary or hourly rate

The goal is to offer clear, transparent insights into salary distribution, departmental staffing, and compensation patterns across the city's workforce.
"""

#--------------------------------------------------------

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

#--------------------------------------------------------

# Calculating the sum of all Salaries in each Division
division_salary_totals = pd.DataFrame(df.groupby('Division Category')['Annual Salary'].sum()).reset_index()

st.space()
st.divider()
st.space()

with st.container():
    st.markdown('<h2 class="pt-0">Salaries by Division Category</h2>', unsafe_allow_html=True)

    salary_cols = st.columns(2, gap="xlarge")

    with salary_cols[0]:
        # st.markdown('<p class="bold">Salary Distribution by Division Category</p>', unsafe_allow_html=True)
        st.markdown(
            """
            City of Memphis employees are organized into four primary categories, each encompassing multiple divisions that deliver related public services, operations, or administrative functions.
            
            Within every category, divisions share common leadership and bring together employees who perform similar work to support the community effectively.
            """
        )
        st.markdown("<p style='font-weight: 600;margin-top:1rem;margin-bottom:0.25rem;line-height:1.0;'>Total Salaries of All Divisions</p>", unsafe_allow_html=True)
        st.markdown(f'<p class="xl-metric left">${total_city_salaries_formatted:,.1f}M<span style="font-size:18px;vertical-align:top;margin-left:0.2rem;">*</span></p>', unsafe_allow_html=True)
        st.caption("<small class='center' style='margin-top:0;line-height:1.0;'>* Does not include part-time, hourly payroll</small>", unsafe_allow_html=True)

    with salary_cols[1]:
        # Sort Divisions by the sum of all Salaries in descending order
        division_salary_totals.sort_values(by='Annual Salary', ascending=False, inplace=True)

        def custom_logic(row):
            return (row['Annual Salary'] / total_city_salaries) 

        # Apply the function to each row (axis=1)
        division_salary_totals['Percentage'] = division_salary_totals.apply(custom_logic, axis=1)

        # Define colors
        color_map = {
            "Public Safety": RED,
            "Public Works": BLUE,
            "Stronger Neighborhoods": GREEN,
            "Good Government": YELLOW,
        }
        
        salary_distribution_by_division_category = alt.Chart(division_salary_totals).mark_arc().encode(
            theta=alt.Theta("Percentage:Q", stack=True),
            color=alt.Color("Division Category:N", scale=alt.Scale(
                domain=list(color_map.keys()),
                range=list(color_map.values())
            )),
            # order=alt.Order("Annual Salary", sort="descending"),
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

    division_category_cols = st.columns(4)

    public_safety_salary = division_salary_totals.loc[
        division_salary_totals['Division Category'] == 'Public Safety', 'Annual Salary'
    ].values[0] / 1e6

    public_works_salary = division_salary_totals.loc[
        division_salary_totals['Division Category'] == 'Public Works', 'Annual Salary'
    ].values[0] / 1e6

    stronger_neighborhoods_salary = division_salary_totals.loc[
        division_salary_totals['Division Category'] == 'Stronger Neighborhoods', 'Annual Salary'
    ].values[0] / 1e6

    good_government_salary = division_salary_totals.loc[
        division_salary_totals['Division Category'] == 'Good Government', 'Annual Salary'
    ].values[0] / 1e6

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
        # Calculating the sum of all Salaries in each Division
        division_salary_totals = pd.DataFrame(df.groupby('Division Name')['Annual Salary'].sum()).reset_index()

        # Sort Divisions by the sum of all Salaries in descending order
        division_salary_totals.sort_values(by='Annual Salary', ascending=False, inplace=True)

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
                RED,
                RED,
                BLUE,
                BLUE,
                BLUE,
                GREEN,
                GREEN,
                BLUE,
                YELLOW,
                YELLOW,
                YELLOW,
                YELLOW,
                YELLOW,
                GREEN,
                YELLOW,
                YELLOW,
                YELLOW,
            ]
        )

        # color="#202124"
        chart = alt.Chart(division_salary_totals).mark_bar().encode(
            x=alt.X('Annual Salary', axis=alt.Axis(title='Annual Salary Total', format='$,s')),
            y=alt.Y(
                'Division Name',
                sort='-x',
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

with st.container():
    st.markdown('<h2 class="pt-0">Employee Workforce Dashboard</h2>', unsafe_allow_html=True)

    overview_col_1, overview_col_2 = st.columns(2, gap="xlarge")

    with overview_col_1:
        st.markdown(
            f"""
            The City of Memphis employs 8,202 individuals across {total_city_job_titles} unique job roles, supporting essential public services throughout the city.
            
            Salaried employees account for over 83% of the City's core full-time workforce, while part-time, hourly employees (typically in seasonal, support, or entry-level roles) make up nearly 17%.

            <div class="table-row">
                <span class="bold">Total employees</span>
                <span>{total_city_employees:,}</span>
            </div>
            <div class="table-row">
                <span class="bold">Full-time (salaried) employees</span>
                <span>{total_salaried_employees:,}</span>
            </div>
            <div class="table-row" style="margin-bottom:1rem;border-bottom:none;">
                <span class="bold">Part-time employees</span>
                <span>{total_part_time_employees:,}</span>
            </div>
            <div class="table-row"">
                <span class="bold">Average annual salary (full-time employees)</span>
                <span>${average_city_salary:,.2f}</span>
            </div>
            <div class="table-row" style="margin-bottom:2rem;">
                <span class="bold">Average hourly rate (part-time employees)</span>
                <span>${average_city_hourly_pay:.2f}</span>
            </div>
            """, unsafe_allow_html=True
        )
        st.caption("<small>Data as of January 28, 2025</small>", unsafe_allow_html=True)

    with overview_col_2:
        source = pd.DataFrame({
            "Employment Type": ["Full-time", "Part-time"],
            "Value": [percent_salaried_employees, percent_part_time_employees],
            "Count": [total_salaried_employees, total_part_time_employees]
        })

        # Define colors
        employee_classification_color_map = {
            "Full-time": "#202124",
            "Part-time": "#9AA0A6"
        }

        pie_chart_job_category = alt.Chart(source).mark_arc().encode(
            theta="Value",
            color=alt.Color("Employment Type", scale=alt.Scale(
                domain=list(employee_classification_color_map.keys()),
                range=list(employee_classification_color_map.values())
            )),
            tooltip=[
                "Employment Type",
                alt.Tooltip("Count:Q", format=",", title="Count"),
                alt.Tooltip("Value:Q", format=".1%", title="Percentage")
            ]
        ).properties(
            title='Employment Type Breakdown'
        )

        st.altair_chart(pie_chart_job_category, width="stretch")

    st.space()

    result = (
        df['Employment Type']
        .groupby(df['Division Name'])
        .value_counts()
        .reset_index(name='Count')
    )

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
                range=[BLACK, GREY]
                
            )),
        tooltip=[
            alt.Tooltip('Division Name:N', title='Division'),
            alt.Tooltip('Employment Type:N', title='Employment Type'),
            alt.Tooltip('sum(Count):Q', title='Count', format=',d')
        ]
    ).properties(
        title=alt.TitleParams(
            text='Employee Count by Division: Full-time vs Part-time',
            subtitle=['Fiscal Year 2025 | Source: City of Memphis'],
            anchor='start'
        )
    )

    st.altair_chart(chart, width="stretch")

# st.header("City Divisions", anchor="city-divisions")
# st.write(
#     """There are a total of 17 divisions for the city of Memphis. Each division is responsible for specific services, operations, or administrative functions. These divisions group employees who perform related work, report under shared leadership, and focus on delivering particular public services or support."""
# )
# st.write(
#     """Employee salaries, job titles, and payroll data are typically categorized and reported by these divisions (as seen in the city's public salary lists and pay plans). This structure helps ensure clear accountability, efficient resource allocation, and alignment with the city's mission to provide essential services to residents."""
# )
# st.write(
#     """City divisions can be grouped together into 6 categories by aligning core responsibilities and typical functions in city operations."""
# )

# df_city_division_categories = pd.DataFrame([
#     {
#         "Category": "Public Safety",
#         'Divisions Included': "Police Services, Fire Services",
#     },
#     {
#         "Category": "Public Works",
#         'Divisions Included': 'Public Works, Solid Waste, City Engineering, General Services',
#     },
#     {
#         "Category": "Stronger Neighborhoods",
#         'Divisions Included': 'Memphis Parks, Library Services, Housing and Community Development',
#     },
#     {
#         "Category": "Good Government",
#         'Divisions Included': 'Executive, Finance and Administration, Human Resources, Information Technology, City Attorney, City Court Clerk, Judicial, Legislative'
#     }
# ])

# st.dataframe(
#     df_city_division_categories,
#     width="stretch",
#     hide_index=True
# )

#--------------------------------------------------------

# st.markdown("#### Salary Totals by Division")

# with st.container(border=True):

#     # Calculating the sum of all Salaries in each Division
#     division_salary_totals = pd.DataFrame(df.groupby('Division Name')['Annual Salary'].sum()).reset_index()

#     # Sort Divisions by the sum of all Salaries in descending order
#     division_salary_totals.sort_values(by='Annual Salary', ascending=False, inplace=True)

#     chart = alt.Chart(division_salary_totals).mark_bar(color=YELLOW).encode(
#         x=alt.X('Annual Salary', axis=alt.Axis(title='Annual Salary Total', format='$0,f')),
#         y=alt.Y(
#             'Division Name',
#             sort='-x',
#             axis=alt.Axis(title=None, labelLimit=300)
#         ),
#         tooltip=[
#             alt.Tooltip('Division Name'),
#             alt.Tooltip('Annual Salary', format="$,.2f")
#         ]
#     ).properties(
#         title='Compensation for Division\'s Salaried Employees',
#     )

#     st.altair_chart(chart, width="stretch")

#--------------------------------------------------------
