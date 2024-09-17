-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `ny-taxi-de-2024-433716.nytaxi.external_green_tripdata_2022`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dataengineering-zoomcamp-bucket/green/green_tripdata_2022-*.parquet']
);

CREATE OR REPLACE TABLE `ny-taxi-de-2024-433716.nytaxi.green_tripdata_2022_materialized` AS
SELECT *
FROM
  `ny-taxi-de-2024-433716.nytaxi.external_green_tripdata_2022`;


--Question 1: What is count of records for the 2022 Green Taxi Data??
select count(*) from `ny-taxi-de-2024-433716.nytaxi.external_green_tripdata_2022`;

/*Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
*/

select count(distinct PULocationID) from `ny-taxi-de-2024-433716.nytaxi.external_green_tripdata_2022`;
select count(distinct PULocationID) from `ny-taxi-de-2024-433716.nytaxi.green_tripdata_2022_materialized`;


-- Question 3: How many records have a fare_amount of 0?
select count(*) from `ny-taxi-de-2024-433716.nytaxi.external_green_tripdata_2022` where fare_amount = 0;


/* 
Question 4:
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)
*/

CREATE OR REPLACE TABLE ny-taxi-de-2024-433716.nytaxi.green_tripdata_2022_partitoned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM ny-taxi-de-2024-433716.nytaxi.external_green_tripdata_2022;


/*
Question 5:
Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?
*/

SELECT DISTINCT(PULocationID)
FROM `ny-taxi-de-2024-433716.nytaxi.green_tripdata_2022_materialized`
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
SELECT DISTINCT(PULocationID)
FROM ny-taxi-de-2024-433716.nytaxi.green_tripdata_2022_partitoned_clustered
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Question 6: Where is the data stored in the External Table you created?
-- Answer : GCP Bucket

-- Question 7: It is best practice in Big Query to always cluster your data:
-- Answer : False

/*
(Bonus: Not worth points) Question 8:
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
*/

SELECT COUNT(*)
FROM `ny-taxi-de-2024-433716.nytaxi.green_tripdata_2022_materialized`

-- O BYTES NOW BECAUSE IT'S CASHED ALREADY
