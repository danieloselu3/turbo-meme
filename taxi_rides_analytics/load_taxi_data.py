import gzip
import requests
import pandas as pd
from io import BytesIO
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
import tempfile
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('taxi_data_loader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Database Configuration
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = ""
SCHEMA_NAME = ""

# GitHub URLs
YELLOW_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
GREEN_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/"

# Years to process
YEARS = ["2019" ,"2020"]
CHUNK_SIZE = 100_000

# Column mapping for each taxi type
COLUMN_MAPPING = {
    'yellow': {
        'VendorID': 'vendorid',
        'tpep_pickup_datetime': 'tpep_pickup_datetime',
        'tpep_dropoff_datetime': 'tpep_dropoff_datetime',
        'passenger_count': 'passenger_count',
        'trip_distance': 'trip_distance',
        'RatecodeID': 'ratecodeid',
        'store_and_fwd_flag': 'store_and_fwd_flag',
        'PULocationID': 'pulocationid',
        'DOLocationID': 'dolocationid',
        'payment_type': 'payment_type',
        'fare_amount': 'fare_amount',
        'extra': 'extra',
        'mta_tax': 'mta_tax',
        'tip_amount': 'tip_amount',
        'tolls_amount': 'tolls_amount',
        'improvement_surcharge': 'improvement_surcharge',
        'total_amount': 'total_amount',
        'congestion_surcharge': 'congestion_surcharge'
    },
    'green': {
        'VendorID': 'vendorid',
        'lpep_pickup_datetime': 'lpep_pickup_datetime',
        'lpep_dropoff_datetime': 'lpep_dropoff_datetime',
        'passenger_count': 'passenger_count',
        'trip_distance': 'trip_distance',
        'RatecodeID': 'ratecodeid',
        'store_and_fwd_flag': 'store_and_fwd_flag',
        'PULocationID': 'pulocationid',
        'DOLocationID': 'dolocationid',
        'payment_type': 'payment_type',
        'fare_amount': 'fare_amount',
        'extra': 'extra',
        'mta_tax': 'mta_tax',
        'tip_amount': 'tip_amount',
        'tolls_amount': 'tolls_amount',
        'improvement_surcharge': 'improvement_surcharge',
        'total_amount': 'total_amount',
        'congestion_surcharge': 'congestion_surcharge'
    }
}

def create_db_engine():
    return create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )

def test_db_connection(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.execute(text(f"SELECT 1 FROM {SCHEMA_NAME}.yellow_tripdata LIMIT 1"))
            conn.execute(text(f"SELECT 1 FROM {SCHEMA_NAME}.green_tripdata LIMIT 1"))
            logging.info("[SUCCESS] Database connection verified")
            return True
    except Exception as e:
        logging.error(f"[ERROR] Database connection failed: {e}")
        return False

def download_file(url, filename):
    try:
        logging.info(f"[INFO] Downloading {filename}")
        response = requests.get(url + filename, stream=True, timeout=60)
        
        if response.status_code == 200:
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, filename)
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logging.info(f"[SUCCESS] Downloaded {filename}")
            return temp_path
        else:
            logging.error(f"[ERROR] Download failed for {filename}")
            return None
    except Exception as e:
        logging.error(f"[ERROR] Download error - {filename}: {e}")
        return None

def process_chunk(chunk, taxi_type, engine, filename):
    try:
        # Rename columns to match PostgreSQL
        chunk.rename(columns=COLUMN_MAPPING[taxi_type], inplace=True)
        
        # Insert data
        table_name = f"{taxi_type}_tripdata"
        chunk.to_sql(table_name, engine, schema=SCHEMA_NAME, 
                    if_exists='append', index=False)
        return len(chunk)
    except Exception as e:
        logging.error(f"[ERROR] Processing error - {filename}: {e}")
        return 0

def process_file(taxi_type, year, month, engine):
    filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
    url = YELLOW_URL if taxi_type == "yellow" else GREEN_URL
    
    temp_path = download_file(url, filename)
    if not temp_path:
        return
    
    try:
        total_rows = 0
        
        with gzip.open(temp_path, 'rt', encoding='utf-8') as f:
            df_iterator = pd.read_csv(f, chunksize=CHUNK_SIZE)
            
            for i, chunk in enumerate(df_iterator):
                rows_inserted = process_chunk(chunk, taxi_type, engine, filename)
                total_rows += rows_inserted
                
                if (i + 1) % 10 == 0:
                    logging.info(f"[PROGRESS] {filename}: {total_rows:,} rows inserted so far")
        
        logging.info(f"[COMPLETE] {filename}: Total {total_rows:,} rows inserted")
    
    except Exception as e:
        logging.error(f"[ERROR] File processing error - {filename}: {e}")
    
    finally:
        try:
            os.remove(temp_path)
            os.rmdir(os.path.dirname(temp_path))
        except Exception as e:
            logging.error(f"[ERROR] Cleanup error - {temp_path}: {e}")

def process_data(taxi_type):
    engine = create_db_engine()
    logging.info(f"[START] Processing {taxi_type} taxi data")
    
    for year in YEARS:
        for month in range(1,13):
            logging.info(f"[PROCESSING] {taxi_type} - {year}-{month:02d}")
            process_file(taxi_type, year, month, engine)
    
    logging.info(f"[FINISHED] Completed {taxi_type} taxi data")

if __name__ == "__main__":
    engine = create_db_engine()
    
    if test_db_connection(engine):
        try:
            # process_data("yellow")
            process_data("green")
        except Exception as e:
            logging.error(f"[ERROR] Fatal error: {e}")
    else:
        logging.error("[ERROR] Exiting due to database connection failure")