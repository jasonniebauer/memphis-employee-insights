import streamlit as st
import pandas as pd
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
    [data-testid="stPageLink-NavLink"][href="good-government"] {
        background: #FEEFC3;
        border-left: 5px solid #FBBC04;
        padding-left: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)


# Main content
st.space()
st.title("Good Government")
st.markdown("### Administration, Finance, HR, IT, Legal, and Governance")