# Data processing utilities

# Library imports
import pandas as pd
from shared.data_loader import initialize_data


# Get data from session state
SOURCE_DF = initialize_data()

def get_division_employment_breakdown(division):
    """"""
    # Make a copy of the original DataFrame
    df = SOURCE_DF.copy()
    # Filter employees to only those in the division specified
    df = df[df['Division Name'] == division]

    # Get total number of employees
    total_employees = len(df)
    # Get total number of full-time employees
    total_full_time_employees = (df['Employment Type'] == 'Full-time').sum()
    # Get total number of part-time employees
    total_part_time_employees = (df['Employment Type'] == 'Part-time').sum()

    # Create DataFrame for categorizing employees by employment type
    return (
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