# Heurist API

Command-line tool for requesting data from Heurist database.

## Install

```console
$ pip install git+https://github.com/LostMa-ERC/heurist-api.git
```

## Run from the command line

The command to dump records from Heurist into validated, flattened files is `heurist dump`.

To specify the record types to export, list each one after the option `-i` (`--id`).

To specify the type of out-file, it requires the following options: `-f` (`--format`), which can be either "csv" or "json," and `-o` (`--outdir`), which is a directory into which the record types' files will be written.

To connect to the Heuirst database, you can either provide your login credentials as options afer the command (`--database`, `--login`, `--password`), or you can store them in an environment variable file, `.env`, which should (a) be in your current working directory / from where you run the command and (b) have the following syntax:

`.env`
```
DB_NAME=your_database
DB_LOGIN=your.login
DB_PASSWORD=your-password
```

Relying on the `.env` file, a command to export records of type 101 and 102 would look like the following:

```console
$ heurist dump -o ./export -f csv -i 101 -i 102
```

### File formats

The `heurist dump` command validates the Heurist data with Pydantic and flattens it, un-nesting Heurist's record pointers and way of structuring geospatial data. The flattened data can then be written to a CSV file or to a line-delimited JSON file.

Example of line-delimited JSON:

```json
{"name_or_title_DType_1": "Anglais", "rec_ID": 26, "rec_TypeID": 102}
{"name_or_title_DType_1": "Anglais – Bueve de Hanstonne", "rec_ID": 37, "rec_TypeID": 102}
```


## Tests

```console
$ pytest tests/
```

## Read into DuckDB

Read either flattened data format into a relational DuckDB database.

### From flattened CSV

```sql
create table 'RECORD' as
	*,
	case when len(foo.split_dates) != 0 then strptime(list_extract(foo.split_dates, 1), '%Y-%m-%d %H:%M:%S') else null end as start_date,
	case when len(foo.split_dates) = 2 then strptime(list_extract(foo.split_dates, 2), '%Y-%m-%d %H:%M:%S') else null end as end_date
from (
	select *, string_split(DATE_COLUMN, '|') as split_dates
	from read_csv('FILE')
) foo
```

### From flattened, line-delimited JSON

```sql
create table 'RECORD' as
select *,
	case when len(DATE_COLUMN) != 0 then strptime(list_extract(DATE_COLUMN, 1), '%Y-%m-%dT%H:%M:%S') else null end as start_date,
	case when len(DATE_COLUMN) = 2 then strptime(list_extract(DATE_COLUMN, 2), '%Y-%m-%dT%H:%M:%S') else null end as end_date
from read_json('FILE')
```