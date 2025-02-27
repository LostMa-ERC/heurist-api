# Download record groups

Before using the `heurist download` command, review the [instructions on how to configure the command-line interface (CLI)](../index.md#configure-the-cli).

**[Logs](./logs.md)** : Don't forget to take advantage of the logs produced by the `heurist download` command! Read about how to check your data and understand the command's results.

## Download multiple record groups' records

```shell
heurist download -f NEW_DATABASE.db -r "My record types" -r "Place, features"
```

If you want to load records from multiple record groups, specify each one with the option `-r` or `--record-group`.

When using this option, the default record group ("My record types") is ignored. Therefore, if you want to download your custom record types, in addition to records types of other groups, do not forget to declare "My record types" too when using the `--record-group` option.

```console
$ heurist download -f NEW_DATABASE.db -r "My record types" -r "Place, features"
Get DB Structure ⠼ 0:00:00
Get Records ━━━━━━━━━━━━ 4/4 0:00:08

Created the following tables
┌───────────────┐
│     name      │
│    varchar    │
├───────────────┤
│ YourRecord_A  │
│ YourRecord_B  │
│ YourRecord_C  │
│ Place         │
│ dty           │
│ rst           │
│ rtg           │
│ rty           │
│ trm           │
├───────────────┤
│    9 rows     │
└───────────────┘
```

## More advanced usage

- [`--outdir`](./export_csv.md) : Export tables to CSV
- [`--user`](./user_filter.md) : Filter by record creator
- [`--require-compound-dates`](./date_validation.md) : Impose strict validation for dates
