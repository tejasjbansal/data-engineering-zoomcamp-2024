import pyarrow as pa
import pyarrow.parquet as pq
import os


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# MANUALLY DEFINE THE CREDENTIALS
# Set the environment variable to the location of the mounted key. json
# This will tell pyarrow where our credentials are
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/personal-gcp.json"

# Define the bucket, project, and table  
bucket_name = 'dataengineering-zoomcamp-mage-bucket'
project_id = 'ny-taxi-de-2024-433716'
table_name = 'green_taxi'          

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):

    # define the pyarrow table and read the df into it
    table = pa.Table.from_pandas(data)

    # define file system - the google cloud object that is going to authorize using the environmental variable automatically
    gcs = pa.fs.GcsFileSystem()

    # write to the dataset using a parquet function
    pq.write_to_dataset(
        table, 
        root_path=root_path, 
        partition_cols=['lpep_pickup_date'], # needs to be a list
        filesystem=gcs
    )

    # Q6 Once exported, how many partitions (folders) are present in Google Cloud?
    print("95")