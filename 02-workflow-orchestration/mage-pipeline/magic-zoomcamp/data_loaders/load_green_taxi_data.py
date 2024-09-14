import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """

    # DEFINE A DICTIONARY OF DATA TYPES FOR THE NON DATETIME COLUMNS 
    taxi_dtypes = {
        'VendorID':pd.Int64Dtype(),
        'passenger_count':pd.Int64Dtype(),
        'trip_distance':float,
        'RatecodeID':float,
        'store_and_fwd_flag':str,
        'PULocationID':pd.Int64Dtype(),
        'DOLocationID':pd.Int64Dtype(),
        'payment_type':pd.Int64Dtype(),
        'fare_amount':float,
        'extra':float,
        'mta_tax':float,
        'tip_amount':float,
        'tolls_amount':float,
        'improvement_surcharge':float,
        'total_amount':float,
        'congestion_surcharge':float
    }

    # CREATE A LIST OF DATETIME COLUMNS.
    # The list will be passed to the read_csv function and pandas will parse the columns as dates with the appropriate time stamps.  
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']  


    # Define the URL template
    url_template = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-{}.csv.gz'

    # Define the months to read data for
    months = [01,02,03,04,05,06,07,08,09,10, 11, 12]

    # Initialize an empty list to store the dataframes
    dfs = []

    # Loop through each month and read the data
    for month in months:
        url = url_template.format(str(month).zfill(2))
        try:
            df = pd.read_csv(url, sep=',', compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
            dfs.append(df)
        except Exception as e:
            print(f"Error reading data for month {month}: {e}")

    # Concatenate all the dataframes
    if dfs:
        result_df = pd.concat(dfs, ignore_index=True)
        print(result_df.head())
    else:
        print("No dataframes to concatenate.")

    # Q1 Once the dataset is loaded, what's the shape of the data?
    print(result_df.shape)
    # read_csv LOADS A CSV FILE INTO A DATAFRAME. THIS BLOCK RETURNS THAT DF. 
    return result_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
