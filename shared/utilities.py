import altair as alt


def employment_type_table(total_employees, total_full_time, total_part_time):
    """
    Table for displaying employee counts by employment type.
    
    :param total_employees: Count of all employees
    :param total_full_time: Count of full-time employees
    :param total_part_time: Count of part-time employees
    """
    return f"""
            <div class="table-row">
                <span class="bold">Full-time (salaried) employees</span>
                <span>{total_employees:,}</span>
            </div>
            <div class="table-row"">
                <span class="bold">Part-time employees</span>
                <span>{total_full_time:,}</span>
            </div>
            <div class="table-row">
                <span class="bold">Total employees</span>
                <span class="bold">{total_part_time:,}</span>
            </div>
            """

def employment_type_pie_chart(df, ft_color, pt_color):
    """
    Pie chart for full-time vs part-time employment.
    
    :param df: DataFrame
    :param ft_color: Color for Full-time pie slice
    :param pt_color: Color for Part-time pie slice
    """
    return alt.Chart(df).mark_arc().encode(
        theta="Value",
        color=alt.Color("Employment Type", scale=alt.Scale(
            domain=['Full-time', 'Part-time'],
            range=[ft_color, pt_color]
        )),
        tooltip=[
            "Employment Type",
            alt.Tooltip("Count:Q", format=",", title="Employees"),
            alt.Tooltip("Value:Q", format=".1%", title="Percentage")
        ]
    )