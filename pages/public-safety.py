import streamlit as st
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
from config import PAGE_CONFIG


# ────────────────────────────────────────────────
# GOOGLE ANALYTICS 4 (GA4)
MEASUREMENT_ID = "G-38Z00YDF0V"

ga_script = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{MEASUREMENT_ID}');
</script>
"""

# Inject invisibly (height=0 hides it)
st.components.v1.html(ga_script, height=0, width=0)
# ────────────────────────────────────────────────

st.set_page_config(**PAGE_CONFIG)

# Render navigation
render_navigation()

# Render reusable styles
render_reusable_styles()

# Get data from session state
df = initialize_data()

# Page-specific CSS (only runs here on page)
st.markdown("""
<style>
    /* Set background color for active page link */
    [data-testid="stPageLink-NavLink"][href="public-safety"] {
        background: #FAD2CF;
        border-left: 5px solid #EA4335;
        padding-left: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.space()
st.title("Public Safety")
st.markdown("### Police, Fire, and Emergency Services")

# # Filter to public safety departments
# safety_depts = ['Police', 'Fire', 'EMS', '911 Communications']
# safety_df = df[df['department'].isin(safety_depts)]

# # Sidebar filters (page-specific)
# with st.sidebar:
#     st.markdown("---")
#     st.subheader("Department Filters")
#     selected_depts = st.multiselect(
#         "Select Departments",
#         # safety_depts,
#         # default=safety_depts,
#         df,
#         default=df,
#         # key="safety_dept_filter"
#     )

# # Apply filters
# if selected_depts:
#     safety_df = safety_df[safety_df['department'].isin(selected_depts)]

# # Metrics
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric("Total Employees", f"{len(safety_df):,}")

# with col2:
#     avg_salary = safety_df['salary'].mean()
#     st.metric("Average Salary", f"${avg_salary:,.0f}")

# with col3:
#     total_cost = safety_df['salary'].sum()
#     st.metric("Total Cost", f"${total_cost/1e6:.1f}M")

# # Department breakdown
# st.subheader("By Department")
# dept_stats = safety_df.groupby('department').agg({
#     'salary': ['count', 'mean', 'median']
# }).round(0)
# st.dataframe(dept_stats, use_container_width=True)

# # Detailed data
# with st.expander("View Employee Details"):
#     st.dataframe(
#         safety_df[['name', 'department', 'title', 'salary']].head(100),
#         use_container_width=True,
#         height=400
#     )