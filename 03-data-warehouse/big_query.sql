-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;


-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `ny-taxi-de-2024-433716.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dataengineering-zoomcamp-bucket/green/green_tripdata_2019-*.csv', 'gs://dataengineering-zoomcamp-bucket/green/green_tripdata_2020-*.csv']
);

-- Check green trip data
SELECT * FROM ny-taxi-de-2024-433716.nytaxi.external_green_tripdata limit 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE ny-taxi-de-2024-433716.nytaxi.green_tripdata_non_partitoned AS
SELECT * FROM ny-taxi-de-2024-433716.nytaxi.external_green_tripdata;


-- Create a partitioned table from external table
CREATE OR REPLACE TABLE ny-taxi-de-2024-433716.nytaxi.green_tripdata_partitoned
PARTITION BY
  DATE(lpep_pickup_datetime) AS
SELECT * FROM ny-taxi-de-2024-433716.nytaxi.external_green_tripdata;

-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM ny-taxi-de-2024-433716.nytaxi.green_tripdata_non_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM ny-taxi-de-2024-433716.nytaxi.green_tripdata_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'green_tripdata_partitoned'
ORDER BY total_rows DESC;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE ny-taxi-de-2024-433716.nytaxi.green_tripdata_partitoned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM ny-taxi-de-2024-433716.nytaxi.external_green_tripdata;

-- Query scans 1.1 GB
SELECT count(*) as trips
FROM ny-taxi-de-2024-433716.nytaxi.green_tripdata_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;

-- Query scans 864.5 MB
SELECT count(*) as trips
FROM ny-taxi-de-2024-433716.nytaxi.green_tripdata_partitoned_clustered
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;