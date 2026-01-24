import streamlit as st


LOGO_URL = "https://files.catbox.moe/eu60ff.png"

def render_navigation():
    """Render consistent navigation sidebar across all pages"""

    st.markdown("""
        <style>
            /* Hide Streamlit's auto-generated navigation */
            [data-testid="stSidebarNav"] {
                display: none;
            }
            
            /* Remove border radius from sidebar logo */
            /* Target the main container for st.image and the image itself */
            [data-testid="stImageContainer"] img {
                border-radius: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Inject custom CSS for per-link background colors
    st.markdown("""
    <style>
        /* Remove default rounded borders */
        [data-testid="stPageLink-NavLink"] {
            border-radius: 0 0.5rem 0.5rem 0;
        }
        
        a[href=""]:hover {
            background: #9AA0A6 !important;        
        }
        a[href="public-safety"]:hover {
            background: #EA4335 !important;
        }
        a[href="public-works"]:hover {
            background: #4285F4 !important;
        }
        a[href="stronger-neighborhoods"]:hover {
            background: #34A853 !important;
        }
        a[href="good-government"]:hover {
            background: #FBBC04 !important;
        }

        [data-testid="stPageLink-NavLink"][href="public-safety"]:hover span,
        [data-testid="stPageLink-NavLink"][href="public-works"]:hover span,
        [data-testid="stPageLink-NavLink"][href="stronger-neighborhoods"]:hover span {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # st.logo(
        #     LOGO_URL,
        #     # link="/", # Optional: adds a hyperlink when clicked
        #     icon_image=LOGO_URL, # Optional: a smaller icon for when the sidebar is collapsed
        #     size="large"
        # )
        st.image(LOGO_URL, width=50)
        st.markdown('<h1 style="padding-top:0;">Memphis Data</h1>', unsafe_allow_html=True)
        st.subheader("City Insights")
        # Navigation links
        st.page_link("streamlit_app.py", label="Overview", icon=":material/tour:")
        st.page_link("pages/public-safety.py", label="Public Safety", icon=":material/local_police:")
        st.page_link("pages/public-works.py", label="Public Works", icon=":material/tram:")  # traffic
        st.page_link("pages/stronger-neighborhoods.py", label="Stronger Neighborhoods", icon=":material/psychiatry:")  # other_houses
        st.page_link("pages/good-government.py", label="Good Government", icon=":material/account_balance:")
        
        st.markdown("---")
        st.caption("Last updated: January 2026")
        st.markdown(
            '<h6>Made by <a href="https://jasonniebauer.com" style="text-decoration:underline;">Jason Niebauer</a></h6>',
            unsafe_allow_html=True,
        )
        