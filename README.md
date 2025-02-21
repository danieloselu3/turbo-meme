# turbo-meme
A Data Engineering Project leveraging DBT, Metabase and Postgres for Analytics Engineering

## Overview

Turbo-Meme is a Data Engineering project that leverages DBT (Data Build Tool) and PostgreSQL for Analytics Engineering. The project aims to process and analyze taxi ride data from New York City, providing insights and analytics through a robust data pipeline.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [DBT Models](#dbt-models)
- [Docker Setup](#docker-setup)
- [Contributing](#contributing)
- [License](#license)

## Project Structure
```
turbo-meme/
├── .gitignore
├── README.md
├── requirements.txt
├── taxi_rides_analytics/
    ├── analyses/
    ├── data/
    ├── dbt_packages/
    ├── dbt_project.yml
    ├── docker-compose.yaml
    ├── load_taxi_data.py
    ├── logs/
    ├── macros/
    ├── metabase-data/
    ├── models/
    ├── seeds/
    ├── snapshots/
    ├── target/
    ├── tests/
    └── tm_venv/
```


## Setup and Installation

### Prerequisites

- Python 3.8+
- Docker
- Docker Compose

### Installation Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/turbo-meme.git
    cd turbo-meme
    ```

2. **Set up the virtual environment:**

    ```sh
    python -m venv tm_venv
    source tm_venv/bin/activate  # On Windows use `tm_venv\Scripts\activate`
    ```

3. **Install Python dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Configure environment variables**

    Update the `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`, and `SCHEMA_NAME` variables in [load_taxi_data.py](http://_vscodecontentref_/3).

## Usage

### Running the Data Pipeline

1. **Start the Docker containers:**

    ```sh
    docker-compose up -d
    ```

2. **Load taxi data:**

    ```sh
    python taxi_rides_analytics/load_taxi_data.py
    ```

    **Disclaimer:** Loading the dataset for the first time will take a very long time, even hours, depending on your computer and internet speed.


3. **Navigate to the DBT project directory:**

    ```sh
    cd taxi_rides_analytics
    ```

4. **For first-time users, initialize the DBT project:**

    ```sh
    dbt init
    ```

5. **Run DBT models:**

    ```sh
    dbt run
    ```

6. **Test DBT models:**

    ```sh
    dbt test
    ```

### Accessing PgAdmin and Metabase

- **PgAdmin:** Access PgAdmin by navigating to `http://localhost:5050` in your web browser. Use the credentials defined in the `docker-compose.yaml` file to log in.
- **Metabase:** Access Metabase by navigating to `http://localhost:3000` in your web browser. Follow the setup instructions to configure Metabase for the first time.


## Data Sources

The project processes taxi ride data from the following sources:

- [NYC TLC Yellow Taxi Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/)
- [NYC TLC Green Taxi Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/)

## DBT Models

### Staging Models

- `stg_green_tripdata`
- `stg_yellow_tripdata`

### Core Models

- `fact_trips`
- `dim_zones`
- `dm_monthly_zone_revenue`

### Macros

- `get_payment_type_description`

## Docker Setup

The project uses Docker to manage dependencies and services. The [docker-compose.yaml](http://_vscodecontentref_/4) file defines the following services:

- **Postgres:** The PostgreSQL database.
- **PgAdmin:** A web-based database management tool for PostgreSQL.
- **DBT:** The DBT container for running models.
- **Metabase:** An open-source business intelligence tool.

### Starting the Services

```sh
docker-compose up -d
```

### Stopping the Services

```sh
docker-compose down
```

## Contributing
We welcome contributions to Turbo-Meme! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add new feature').
5. Push to the branch (git push origin feature-branch).
6. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

