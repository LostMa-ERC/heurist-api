# Integrate with R-studio

One reason for choosing DuckDB as a pivot format is that it features a suite of clients that let you connect to the database and conduct your analyses in multiple programming languages, including Python, Node.js, R, and Java.

## [DuckDB's R Client](https://duckdb.org/docs/stable/clients/r.html)

### Python set up

To work with Heurist data in R, first generate the DuckDB database file using the Python command-line tool.

#### Install the CLI

- [Install](./index.md#installation) the `heurist` Python package.

#### Extract, transform, load

- Execute the [`download`](./download//index.md#basic-usage-my-record-types) command.

```shell
heurist -d YOUR_DATABASE -l "your.login" -p "your-password" download -f heurist.duckdb
```

### R set up

Then, follow DuckDB's [instructions](https://duckdb.org/docs/stable/clients/r.html) for connecting to the DuckBD database file in R.

#### [Install](https://duckdb.org/docs/installation/?version=stable&environment=r) the R Client

- Install the DuckDB R Client.

```r
install.packages("duckdb")
```

#### Connect to the DuckDB database

Using the file path given in the `heurist download` command, i.e. `heurist.duckdb`, connect to the database file.

```r
# Load the duckdb package
library("duckdb")

# Connect to the database file
con <- dbConnect(duckdb(), dbdir = "heurist.duckdb", read_only = FALSE)
```

#### Execute SQL queries in R

Execute SQL queries.

```r
res <- dbGetQuery(con, "SELECT * FROM MyHeuristRecord")
```
