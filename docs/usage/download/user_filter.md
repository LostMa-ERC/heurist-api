# Download record groups

Before using the `heurist download` command, review the [instructions on how to configure the command-line interface (CLI)](../index.md#configure-the-cli).

**[Logs](./logs.md)** : Don't forget to take advantage of the logs produced by the `heurist download` command! Read about how to check your data and understand the command's results.

## Download records based on creator

```shell
heurist download -f NEW_DATABASE.db -u 12
```

If you want to load only a selection of records based on who created them, specify the user's Heurist ID with the option `-u` or `--user`.

All users with access to the Heurist database are given a unique ID. You can see this information on the `Users` tab of Heurist's `Admin` panel.

![Screenshot of Heurist, showing "Admin" panel and the "Users" tab.](../../assets/heurist-admin-panel-users.png)

The `--user` option can be repeated to load records for multiple users together in a DuckDB database.

```shell
heurist download -f NEW_DATABASE.db -u 12 -u 17
```

## More advanced usage

- [`--outdir`](./export_csv.md) : Export tables to CSV
- [`--record-group`](./group_types.md) : Record group types
- [`--require-compound-dates`](./date_validation.md) : Impose strict validation for dates
