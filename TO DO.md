# To do
[ ] top/lowest paid position from each division
[ ] division category percentage of city total
[ ] division salaries as percent of all city salaries
[ ] average salary per division
[ ] avg salary across the city
[ ] avg hourly pay per division vs for the city
[ ] percent of each division is salaried vs part-time
[ ] number of unique jobs/roles per division


TOP 20 PERFORMANCE OPTIMIZATIONS:

1. ✅ Use st.navigation() (modern, lightweight approach)
2. ✅ Initialize session state once at app start
3. ✅ Add static sidebar content before navigation
4. ✅ Define configuration constants once
5. ✅ Use @st.cache_data for data loading with TTL
6. ✅ Optimize pandas dtypes (category, int32 vs int64)
7. ✅ Cache expensive computations separately
8. ✅ Use @st.cache_resource for connections
9. ✅ Lazy load heavy dependencies
10. ✅ Store data in session_state to avoid reloading
11. ✅ Use categorical.categories for filter options
12. ✅ Use boolean indexing for filtering
13. ✅ Prefer st.columns over containers
14. ✅ Use tabs to defer rendering
15. ✅ Limit dataframe rows with height parameter
16. ✅ Provide downloads for large datasets
17. ✅ Create reusable chart templates
18. ✅ Aggregate data before plotting
19. ✅ Sample large datasets for visualization
20. ✅ Use parquet instead of CSV for large files

AVOID:
❌ Old pages/ folder approach (slower imports)
❌ Loading data on every rerun
❌ Using classes for pages (adds overhead)
❌ Rendering thousands of rows in dataframes
❌ Creating charts from raw data without aggregation
❌ Importing heavy libraries at module level
❌ Using st.experimental_rerun() unnecessarily
❌ Deep nesting of containers
❌ Displaying all data when filtering is needed

# ====================
# WHY page_modules/ IS MOST PERFORMANT
# ====================

OLD APPROACH (pages/ folder):
❌ Streamlit auto-discovers .py files in pages/
❌ Each file runs on import (slower)
❌ Files named like: pages/1_📊_Dashboard.py
❌ Less control over execution
❌ Can't easily share state between pages

NEW APPROACH (st.navigation() + modules):
✅ You explicitly import only what you need
✅ Functions, not full file execution
✅ Better control over when code runs
✅ Easier to share data via session_state
✅ Cleaner organization
✅ FASTER - only imports function references


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