import pandas as pd
from sqlalchemy import create_engine
from time import time    
import argparse
import os

def ingest(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'data.csv.gz'

    os.system(f'wget {url} -O {csv_name}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, compression='gzip', iterator=True, chunksize=100000, low_memory=False)
    c = 0

    for df in df_iter:
        t_start = time()
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        if (c == 0):
            # Create _yellow_taxi_data_ table with headers only
            df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()
        c+=1
        print(f'Inserted chunk number {c}, took {t_end - t_start} seconds')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write data to')
    parser.add_argument('--url', help='url of the csv.gz file')

    args = parser.parse_args()
    ingest(args)
