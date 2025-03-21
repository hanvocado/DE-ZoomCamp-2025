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
```sql
\dt
select count(1) from yellow_taxi_data;
```
There are 1369765 records.

## Connecting pgAdmin and Postgres
To make it more convenient to access and manage our databases, we will use _pgAdmin_. It's possible to run pgAdmin as a container along with the Postgres container, but both containers will have to be in the same virtual network so that they can find each other.

👉 Create a Docker network called _pg-network_
```bash
docker network create pg-network
```

👉 Re-run Postgres container
We will add the docker network name and name this container `pg-database`. The container name is neccessary, later we will use it in pgAdmin to access this particular container.

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
``` 

👉 Run pgAdmin container
```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    dpage/pgadmin4
```

👉 Connect pgAdmin to pg-database
* Access pgAdmin: [localhost:8080](localhost:8080)
* Register Server: 
    * Right-click on Servers on the left sidebar and select Register > Server...
    * Under _General_ section, give the Server a name
    * Under _Connection_ section, add the same host name, user and password used when running the postgres container.

👉 Save and explore

## Dockerizing the Ingestion Script
In the [Ingesting NY Taxi Data section](#ingesting-ny-taxi-data-to-postgres), we directly run jupyter notebook to ingest data. In this section, we will build our docker image to run ingestion script

👉 Convert `upload-data.ipynb` to python script
```bash
jupyter nbconvert --to=script upload-data.ipynb
```
I got this error: `bash: /usr/bin/jupyter: No such file or directory`. This is because my system is prioritizing `/usr/bin` in its PATH variable before `/home/xxx/.local/bin`, where my actual jupyter installation resides. I did this to fix it: 

```bash
echo 'export PATH=/home/xxx/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

👉 Edit the script
* Pass arguments to the script using `argparse`
* Make the script download data instead of reading file from host file system
* Refactor

👉 Test the script
Before running it in docker container, make sure the ingestion script works

* Drop `yellow_taxi_data` table
```sql
DROP TABLE yellow_taxi_data;
```

* Run the script
```bash
python3 ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```

* Go to pgAdmin and check

👉 Write Dockerfile
```Dockerfile
FROM python:3.10

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
```

👉 Build docker image
```bash
docker build -t taxi_ingest:1.0 .
```

👉 Run container
```bash
docker run -it \
    --network=pg-network \
    taxi_ingest:1.0 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```

* `--network`: this container and the postgres container have to run on the same docker network so they can find each other.
* `taxi_ingest:1.0`: the docker image name.
* The rest parameters is for our ingestion job. `host` now is `pg-database`, which is the name of postgres container running in `pg-network`. `localhost` is the container itself, postgresql is not running in this container but in `pg-database` container.

## Running Postgres and pgAdmin with Docker-Compose
To make it more convenient to run multiple containers with just one config file.

👉 Create `docker-compose.yaml`

👉 Run services
```bash
docker-compose up
```

I got **Permission denied: '/var/lib/pgadmin/sessions'**.
Solution: Make the services run with the same UID/GID as host user
* Create `.env` file, UID and GID variable will have the same value as host user

```bash
echo "UID=$(id -u)" > .env
echo "GID=$(id -g)" >> .env
```

* Add `user` and `env_file` variables to [docker-compose](./docker_sql/docker-compose.yml) file

Now pgdatabase and pgadmin services are up, if you want to re-run `taxi_ingest` container, use `docker network ls` to find the network these services are running on.

## Terraform

Terraform: An infrastructure as code tool
Example: terraform on our local machine will tell GCP who we are and what access we have to create resources.

Pre-Requisites:
* [Install Terraform](https://developer.hashicorp.com/terraform/install)

* Create GCP account

I had error about payment method while creating GCP account so I will temporarily stop at this for this module.