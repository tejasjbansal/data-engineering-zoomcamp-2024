import pandas as pd
import numpy as np
import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    # Q2 Upon filtering the dataset where the passenger count is greater than 0 and the trip distance is greater than zero, how many rows are left?
    print(data.shape[0])

    data['lpep_pickup_date'] = pd.to_datetime(data['lpep_pickup_datetime'])

    # Q3 Which of the following creates a new column lpep_pickup_date by converting lpep_pickup_datetime to a date?
    data['lpep_pickup_date'] = data['lpep_pickup_date'].dt.date

    # Q4 What are the existing values of VendorID in the dataset?
    print(data['VendorID'].unique())

    # Rename columns
    old_columns = data.columns
    data.columns = [camel_to_snake(col) for col in data.columns]

    # Q5 How many columns need to be renamed to snake case?
    series1 = pd.Series(old_columns)
    series2 = pd.Series(data.columns)

    comparison = np.where(series1 == series2, 'Equal', 'Not Equal')
    not_equal_count = np.sum(comparison == 'Not Equal')
    print(comparison)  # Output: ['Equal' 'Equal' 'Not Equal' 'Equal' 'Equal']
    print(not_equal_count)

    # print(data.head())
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # Assertions
    assert output['vendor_id'].isin(output['vendor_id']).all(), "vendor_id contains invalid values"
    assert (output['passenger_count'] > 0).all(), "passenger_count must be greater than 0"
    assert (output['trip_distance'] > 0).all(), "trip_distance must be greater than 0"
