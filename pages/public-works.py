import streamlit as st
import pandas as pd
from shared.navigation import render_navigation
from shared.styles import render_reusable_styles
from shared.data_loader import initialize_data
from config import PAGE_CONFIG


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
    [data-testid="stPageLink-NavLink"][href="public-works"] {
        background: #D2E3FC;
        border-left: 5px solid #4285F4;
        padding-left: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)


# Main content
st.space()
st.info(
    'Building Better Transparency: Under Active Development – Check Back for More Soon!',
    icon=":material/build:"
)
st.title("Public Works")
st.markdown("### Public Works, Solid Waste Management, City Engineering, and General Services")