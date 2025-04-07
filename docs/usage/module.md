# Python API Client

Before using the `heurist` module, review the [instructions on how to install the Python package](./index.md#installation).

## Demos

Explore Jupyter notebooks in the GitHub repository's folder [`demos/`](https://github.com/LostMa-ERC/heurist-etl-pipeline/tree/main/demos).

## Coding with the ETL workflow

You can integrate a Heurist database's tables into your Python application with just **_3 lines of code_**! (But 1 line will be really long, so we break it up for readability.)

### 1. Create a DuckDB connection

Create a connection to a [DuckDB database](https://duckdb.org/docs/stable/clients/python/overview.html).

```python
import duckdb

# Line 1 : DuckDB connection
conn = duckdb.connect()
```

To preserve the data that `heurist` extracts, transforms, and loads into the database, give the `connect()` method a path to a file, i.e. `duckdb.connect("heurist.db")`. If no argument is provided, `duckdb.connect()` creates an in-memory database connection.


### 2. Open a `HeuristAPIConnection`

To optimise your connection to the Heurist database, we will log in only one time and keep that connection live as a Python context.

Use your login credentials to create a `HeuristAPIConnection` context, which returns a client.

```python
from heurist.api.connection import HeuristAPIConnection

# Line 2 (broken for readability) : API Connection
with HeuristAPIConnection(
    db = HEURIST_DATABASE,
    login = HEURIST_LOGIN,
    password = HEURIST_PASSWORD
) as client:
    _ # ... see below code block
```

### 3. Run the ETL process

```python
from heurist.workflows import extract_transform_load

# Line 2 (broken for readability) : API Connection
with HeuristAPIConnection(
    # ... see above code block
) as client:
    # Line 3 : ETL process
    extract_transform_load(client = client, duckdb_connection = conn)
```

To load all your custom records, meaning all those of types in your "My record types" group, run the `extract_transform_load()` function with all its defaults, simply providing your (1) API connection and (2) DuckDB connection.

To explore all of the `extract_transform_load` function's parameters, see the [source code](../reference/workflows/etl.md).

#### Summary

See all 3 lines of code in action below:

```python
import duckdb
from heurist.api.connection import HeuristAPIConnection
from heurist.workflows import extract_transform_load

# Line 1 : DuckDB connection
conn = duckdb.connect()

# Line 2 (broken for readbility) : API connection
with HeuristAPIConnection(
    db = HEURIST_DATABASE,
    login = HEURIST_LOGIN,
    password = HEURIST_PASSWORD
) as client:
    # Line 3 : ETL process
    extract_transform_load(client = client, duckdb_connection = conn)
```

#### Multiple record type groups

If you want to recover records of types in multiple record type groups, list all of them in the `record_group_names` parameter.

```python
extract_transform_load(
    client = client,
    duckdb_connection = conn,
    record_group_names = ("My record types", "Place, features")
)
```

#### Check your data's validation

Running the `extract_transform_load` function causes log files to be generated.

Read the `./validation.log` file to review all the records in the Heurist database that did not pass the data validation and were not loaded into the DuckDB database. For more information, see the section on [logs](./download/logs.md).

## DuckDB Python as a pivot format

Having loaded the Heurist records into a DuckDB database, you can begin taking advantage of [DuckDB's Python client](https://duckdb.org/docs/stable/clients/python/overview.html).

### Heurist DuckDB -> to something else

#### Pandas dataframe

DuckDB can convert all of its relations (tables, query results, etc.) into `pandas` dataframes with `df()`. Because many data science techniques and methods are used to `pandas`, this is a very useful way to interact with the Heurist data and one of the reasons the `heurist` package uses DuckDB as a pivot format.

Convert a Heurist table, which has been loaded into the DuckDB database, into a `pandas` dataframe.

```console
>>> conn.table("Witness").df()
      H-ID  type_id  ...  review_status TRM-ID             review_note
0    47500      105  ...                  9697                  Check.
1    47897      105  ...                  9697                  Check.
2    47756      105  ...                  9697                  Check.
3    47978      105  ...                  9697                  Check.
4    47552      105  ...                  9697                  Check.
..     ...      ...  ...                   ...                     ...
168  48051      105  ...                  9697  Kienhorst zegt in BNM?
169  47458      105  ...                  9697                    Ref.
170  47454      105  ...                  9697                    Ref.
171  47433      105  ...                  9697             Check, ref.
172  47420      105  ...                  9697           Check, ghost.

[173 rows x 36 columns]
```

Or convert SQL query results into a `pandas` dataframe.

```console
>>> conn.sql('SELECT * FROM Witness w JOIN TextTable t ON w."is_manifestation_of H-ID" = t."H-ID"').df()
      H-ID  type_id  ...  review_status TRM-ID_1 review_note_1
0    47792      105  ...                  9697.0        Check.
1    48339      105  ...                  9697.0         Check
2    47906      105  ...                  9697.0        Check.
3    48356      105  ...                  9697.0         Check
4    47912      105  ...                  9697.0        Check.
..     ...      ...  ...                     ...           ...
168  47742      105  ...                  9697.0        Check.
169  47738      105  ...                  9697.0        Check.
170  47725      105  ...                  9697.0        Check.
171  47734      105  ...                  9697.0        Check.
172  47637      105  ...                  9697.0        Check.

[173 rows x 89 columns]
```

#### Parquet, CSV files

DuckDB's Python client also lets you export relations into modern file formats commonly used in data science, notably CSV and parquet.

```python
# Execute some SQL query on your database,
# storing the result in a relation object
rel = conn.sql("SELECT * FROM TextTable LIMIT 10")

# Write the result to a csv file
rel.write_csv("my_results.csv")

# Write the result to a parquet file
rel.write_parquet("my_results.parquet")
```

### Something else -> Heurist DuckDB

DuckDB's Python client can also ingest data from other sources and Python objects. This is useful if you want to enrich / complement your Heurist data with information not available in your Heurist database.

[Read](https://duckdb.org/docs/stable/clients/python/data_ingestion) about DuckDB's Python data ingestion.

#### Other data files

You can create new tables or views in your database by reading datasets from external files.

```python
conn.execute("CREATE TABLE OtherDataset AS SELECT * FROM read_csv('other_dataset.csv')")
```

```python
conn.execute("CREATE TABLE OtherDataset AS SELECT * FROM read_parquet('other_dataset.parquet')")
```

```python
conn.execute("CREATE TABLE OtherDataset AS SELECT * FROM read_json('other_dataset.json')")
```

Then, from within your database connection, you can join your Heurist data with the external dataset.

```python
sql = """
SELECT *
FROM MyHeuristRecord h
LEFT JOIN OtherDataset o
    ON h.url = o.url
"""
rel = conn.sql(sql)
```

#### Other dataframes

In your DuckDB database connection, you can also select dataframes you've created with `pandas` and join them with your Heurist data.

```python
import pandas as pd

new_dataframe = pd.DataFrame.from_dict({
    "insee_2025_population_total_all": [76_452, 1_663_974],
    "insee_2025_population_total_women": [38_173, 868_376],
    "name": ["Lozère", "Hautes-de-Seine"]
})
rel = conn.sql("""
SELECT *
FROM new_dataframe df
JOIN MyHeuristRecord h
    ON df.name = h.department
""")
```
