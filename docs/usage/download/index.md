# Download record groups

Before using the `heurist download` command, review the [instructions on how to configure the command-line interface (CLI)](../index.md#configure-the-cli).

**[Logs](./logs.md)** : Don't forget to take advantage of the logs produced by the `heurist download` command! Read about how to check your data and understand the command's results.

## Basic usage: My record types

```shell
heurist download -f NEW_DATABASE.db
```

By default, without specifying any target record groups, `heurist download` will download all the records you created in the "My record types" group. The only requirement is a path to the file for loading the results in a DuckDB database, indicated with the `-f` option.

```console
$ heurist download -f NEW_DATABASE.db
Get DB Structure ⠼ 0:00:00
Get Records ━━━━━━━━━━━━ 3/3 0:00:08

Created the following tables
┌───────────────┐
│     name      │
│    varchar    │
├───────────────┤
│ YourRecord_A  │
│ YourRecord_B  │
│ YourRecord_C  │
│ dty           │
│ rst           │
│ rtg           │
│ rty           │
│ trm           │
├───────────────┤
│    8 rows     │
└───────────────┘
```

The tables with lower-case names are Heurist's way of organising information about all the record types (`rty`, `rtg`), data fields (`dty`, `rst`), and vocabularies (`trm`) in the database. They're made available in case you want to access that structural information during your analysis / use of the extracted, transformed, and loaded data.

## More advanced usage

- [`--outdir`](./export_csv.md) : Export tables to CSV
- [`--record-group`](./group_types.md) : Record group types
- [`--user`](./user_filter.md) : Filter by record creator
- [`--require-compound-dates`](./date_validation.md) : Impose strict validation for dates
