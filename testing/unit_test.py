import pandas as pd
from datetime import datetime

def test_clean_age_column():
    '''Test the clean_age_column function from src.DC_columns'''

    test_input = '24_'
    actual_output = 24

    test_input = test_input.rstrip('_')
    expected_output = int(test_input)

    assert expected_output == actual_output

def convert_month_name_to_num(mname: str):
    '''This is the function convert the month name into month value'''
    mname = datetime.strptime(mname, '%B').month
    return mname

def test_process_month():
    '''Test the process_month function from src.FE_categorical_columns'''
    '''Create the new column, month_num by apply the function to convert the month name into month value'''

    test_input = 'December'  
    expected_output = 12 

    actual_output = convert_month_name_to_num(test_input)
    assert actual_output == expected_output
