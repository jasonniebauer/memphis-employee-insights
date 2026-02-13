import altair as alt


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