# Download record groups

Before using the `heurist download` command, review the [instructions on how to configure the command-line interface (CLI)](../index.md#configure-the-cli).

**[Logs](./logs.md)** : Don't forget to take advantage of the logs produced by the `heurist download` command! Read about how to check your data and understand the command's results.

## Export download to CSV files

```shell
heurist download -f NEW_DATABASE.db -o OUTDIR/
```

By declaring the path to a directory (`--outdir`, `-o`), in addition to the required DuckDB database file path (`-f`), you can export the record tables loaded into DuckDB.

Each CSV file name is identical with the table's name in the DuckDB database. In case your Heurist records have names that are not SQL-safe, and therefore were transformed during `heurist download`, check the `logs/tables.log.tsv` to review how your tables have been called.

### Example Output

For example, if we called `heurist download` with the option `-o ./tables`, a Heurist record type named `genre` would yield the CSV `./tables/Genre.csv`. All record tables would created in the directory `./tables`.

|H-ID|type_id|preferred_name|parent_genre H-ID|alternative_names|description|described_at_URL|
|---|---|---|---|---|---|---|
|44167|117|chanson de geste||[]|Long epic poem from the Middle Ages.|['https://www.wikidata.org/wiki/Q651019', 'https://catalogue.bnf.fr/ark:/12148/cb11947470n']|
|46366|117|riddarasögur||[chivalric sagas]|The riddarasögur are Norse prose sagas of the romance genre.|[]|
|46367|117|riddarasögur indigenous|46366|[]|Icelandic indigenous creations in a style of riddarasögur.|[]|
|46370|117|riddarasögur translated|46366|[]|Norse translations of French chansons de geste and Latin romances and histories.|[]|

## More advanced usage

- [`--record-group`](./group_types.md) : Record group types
- [`--user`](./user_filter.md) : Filter by record creator
- [`--require-compound-dates`](./date_validation.md) : Impose strict validation for dates
