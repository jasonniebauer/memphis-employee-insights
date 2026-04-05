# ====================
# Efficient Data Loading with Caching
# ====================
import streamlit as st
import pandas as pd


def get_city_division_category(row):
    division = row['Division Name']
    public_safety = ['Police Services', 'Fire Services']
    public_works = ['Public Works', 'Solid Waste', 'City Engineering', 'General Services']
    stronger_neighborhoods = ['Memphis Parks', 'Library Services', 'Housing and Community Development']
    good_government = ['Executive', 'Finance and Administration', 'Human Resources', 'Information Technology', 'City Attorney', 'City Court Clerk', 'Judicial', 'Legislative']

    if division in public_safety:
        return 'Public Safety'
    elif division in public_works:
        return 'Public Works'
    elif division in stronger_neighborhoods:
        return 'Stronger Neighborhoods'
    elif division in good_government:
        return 'Good Government'
    else:
        return

@st.cache_data(ttl=3600, show_spinner="Loading salary data...")
def load_salary_data() -> pd.DataFrame:
    """Load salary data - cached globally"""
    df = pd.read_csv('data/City of Memphis Employee Salaries 2025.csv')
    
    # Categorize city divisions/departments
    df['Division Category'] = df.apply(get_city_division_category, axis=1)

    # Rename Category column to Employment Type
    df = df.rename(columns={'Category': 'Employment Type'})
    # Replace 'Regular' with 'Full-time' in the Employment Type column
    df['Employment Type'] = df['Employment Type'].replace('Regular', 'Full-time')
    # Replace 'Part-Time' with 'Part-time' in the Employment Type column
    df['Employment Type'] = df['Employment Type'].replace('Part-Time', 'Part-time')
    
    return df

@st.cache_data(ttl=3600)
def get_department_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute department statistics - cached"""
    return df.groupby('department').agg({
        'salary': ['count', 'mean', 'median', 'min', 'max']
    }).round(0)

def initialize_data():
    """Initialize data in session state"""
    if 'salary_data' not in st.session_state:
        st.session_state.salary_data = load_salary_data()
    return st.session_state.salary_data
