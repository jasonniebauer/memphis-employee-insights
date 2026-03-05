# To do
[ ] division category percentage of city total
[ ] division salaries as percent of all city salaries
[ ] average salary per division
[ ] avg hourly pay per division vs for the city
[ ] percent of each division is salaried vs part-time
[ ] number of unique jobs/roles per division
[ ] top paying job/role
[ ] lowest paying job/role
[ ] average hourly rate
[ ] average salary

PERFORMANCE OPTIMIZATIONS:

✅ Initialize session state once at app start
✅ Use @st.cache_data for data loading with TTL
✅ Optimize pandas dtypes (category, int32 vs int64)
✅ Cache expensive computations separately
✅ Use @st.cache_resource for connections
✅ Store data in session_state to avoid reloading
✅ Create reusable chart templates

# ====================
# pages/dashboard.py - Efficient Page Structure
# ====================
"""
import streamlit as st
import pandas as pd
from data.loader import load_salary_data, compute_department_stats
from utils.charts import create_bar_chart, create_line_chart

def dashboard_page():
    '''Dashboard page function'''
    
    st.title("📊 Salary Dashboard")
    
    # ✅ PERFORMANCE TIP #10: Use session state for expensive operations
    # Only load data if not already loaded
    if 'salary_data' not in st.session_state:
        st.session_state.salary_data = load_salary_data('salaries.parquet')
    
    df = st.session_state.salary_data
    
    # ✅ PERFORMANCE TIP #11: Create sidebar filters efficiently
    with st.sidebar:
        st.subheader("Filters")
        
        # Use unique() on category columns (faster than sorted)
        departments = st.multiselect(
            "Department",
            options=df['department'].cat.categories,  # Faster for categorical
            default=None
        )
        
        salary_range = st.slider(
            "Salary Range",
            int(df['salary'].min()),
            int(df['salary'].max()),
            (int(df['salary'].min()), int(df['salary'].max()))
        )
    
    # ✅ PERFORMANCE TIP #12: Filter data efficiently using boolean indexing
    mask = (df['salary'] >= salary_range[0]) & (df['salary'] <= salary_range[1])
    if departments:
        mask &= df['department'].isin(departments)
    
    filtered_df = df[mask]
    
    # ✅ PERFORMANCE TIP #13: Use columns for layout (renders faster than containers)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Employees", f"{len(filtered_df):,}")
    with col2:
        avg_salary = filtered_df['salary'].mean()
        st.metric("Avg Salary", f"${avg_salary:,.0f}")
    with col3:
        median_salary = filtered_df['salary'].median()
        st.metric("Median Salary", f"${median_salary:,.0f}")
    with col4:
        total_payroll = filtered_df['salary'].sum()
        st.metric("Total Payroll", f"${total_payroll:,.0f}")
    
    # ✅ PERFORMANCE TIP #14: Use tabs to defer rendering
    tab1, tab2, tab3 = st.tabs(["Overview", "Department Analysis", "Details"])
    
    with tab1:
        # Only renders when tab is active
        fig = create_bar_chart(filtered_df, 'department', 'salary')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        dept_stats = compute_department_stats(filtered_df)
        st.dataframe(dept_stats, use_container_width=True, height=400)
    
    with tab3:
        # ✅ PERFORMANCE TIP #15: Use st.dataframe with height limit
        # Don't render all rows at once for large datasets
        st.dataframe(
            filtered_df.head(1000),  # Limit rows
            use_container_width=True,
            height=600
        )
        
        # ✅ PERFORMANCE TIP #16: Provide download option instead of showing all
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "Download Full Dataset",
            csv,
            "salaries.csv",
            "text/csv",
            key='download-csv'
        )