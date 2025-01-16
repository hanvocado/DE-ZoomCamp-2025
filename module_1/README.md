# Module 1: Basics and Setups

## Docker

A **Docker image** is a _snapshot_ of a container that we can define to run our software, or in this case our data pipelines. By exporting our Docker images to Cloud providers such as Amazon Web Services or Google Cloud Platform we can run our containers there.

Docker containers are ***stateless***: any changes done inside a container will not be saved when the container is killed and started again. This is an advantage because it allows us to restore any container to its initial state in a reproducible manner.

### Getting started with Docker

👉 Write Dockerfile

👉 Build Docker image:
```bash
docker build -t [image-name] [directory]
```

👉 Run container:
```bash
docker run [image-name] [arg]
```

## Ingesting NY Taxi Data to Postgres

👉 Create a folder where Postgres will store data

👉 Run Postgres container
```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```

This container includes everything necessary to run PostgreSQL independently of our local system.

* Environment variables:
    * `POSTGRES_USER`: username for logging into the database.
    * `POSTGRES_PASSWORD`: the user's password.
    * `POSTGRES_DB`: database name.
* `-v` points to the volume directory. It will map a folder in host file system (before `:`) to a folder in the container (after `:`). Even though Docker is stateless, this will make sure our data is consistent. Change the paths according to your setup.
* `-p` is for port mapping. We map the default Postgres port to the same port in the host.
* The last argument is the image name and tag. We run the official `postgres` image on its version `13`.

👉 Connect to **ny_taxi** database using pgcli
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
The password is not provided, it will be requested after this command.

👉 Ingest data to Postgres using pandas and sqlalchemy

* Download data:
```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

[Data Dictionary – Yellow Taxi Trip Records](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)

* Unzip the file: 
```bash
gzip -d yellow_tripdata_2021-01.csv.gz
```

Option -d will delete the .csv.gz file after unzipping.

* Run jupyter notebook
```bash
pip3 install notebook
jupyter-notebook
```
* Write and run _upload-data.ipynb_

* Test
In pgcli terminal, run these commands to check if data is there in ny_taxi database
```bash
\dt
select count(1) from yellow_taxi_data;
```
There are 1369765 records.

