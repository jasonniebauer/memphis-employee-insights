# Data processing utilities

# Library imports
import pandas as pd
from shared.data_loader import initialize_data


# Get data from session state
SOURCE_DF = initialize_data()

def get_division_details(division):
    """"""
    # Make a copy of the original DataFrame
    df = SOURCE_DF.copy()

    # Check if division a category from Good Government
    if division in ['Governance', 'Legal']:
        # Define Governance and Legal category groups of divisions
        governance = ['Executive', 'Legislative', 'Judicial']
        legal = ['City Attorney', 'City Court Clerk']

        # Filter employees to only those in the category specified
        if division == 'Governance':
            df = df[df['Division Name'].isin(governance)]
        elif division == 'Legal':
            df = df[df['Division Name'].isin(legal)]
    else:    
        # Filter employees to only those in the division specified
        df = df[df['Division Name'] == division]

    # Get the highest salary for the division
    max_salary = df['Annual Salary'].max()
    # Get the lowest salary for the division
    min_salary = df['Annual Salary'].min()
    # Get the job paying the highest salary
    top_paying_job = df.loc[df['Annual Salary'].idxmax(), 'Job Title']
    # Get the highest hourly rate
    max_hourly_rate = df['Hourly/Per Event Rate'].max()
    # Get the lowest hourly rate
    min_hourly_rate = df['Hourly/Per Event Rate'].min()
    # Get the job paying the highest hourly rate
    top_paying_part_time_job = df.loc[df['Hourly/Per Event Rate'].idxmax(), 'Job Title']
    # Get the average of all annual salaries
    average_salary = df['Annual Salary'].mean()
    # Get the average of all hourly rates
    average_hourly_rate = df['Hourly/Per Event Rate'].mean()
    # Get the total number of unique jobs
    total_unique_jobs = len(df['Job Title'].unique())
    # Get total number of employees
    total_employees = len(df)
    # Get total number of full-time employees
    total_full_time_employees = (df['Employment Type'] == 'Full-time').sum()
    # Get total number of part-time employees
    total_part_time_employees = (df['Employment Type'] == 'Part-time').sum()

    # Create DataFrame for categorizing employees by employment type
    return (
        top_paying_job,
        max_salary,
        min_salary,
        top_paying_part_time_job,
        max_hourly_rate,
        min_hourly_rate,
        average_salary,
        average_hourly_rate,
        total_unique_jobs,
        total_employees,
        total_full_time_employees,
        total_part_time_employees,
        pd.DataFrame({
            "Employment Type": ["Full-time", "Part-time"],
            "Value": [
                total_full_time_employees / total_employees,
                total_part_time_employees / total_employees
            ],
            "Count": [
                total_full_time_employees,
                total_part_time_employees
            ]
        })
    )