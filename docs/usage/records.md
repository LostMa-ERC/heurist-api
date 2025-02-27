# Export a record type

Before using the `heurist record` subcommand, review the [instructions on how to configure the command-line interface (CLI)](./index.md#configure-the-cli).

> Documentation is under development.

```console
heurist record -t RECORD_TYPE_ID_NUMBER
```

Specify the targeted record type with the option `-t` or `--record-type`. The subcommand `record` will call Heurist's API and download the type's records in Heurist's JSON export.

```shell
$ heurist record -t 101
Get Records of type 101 ⠋ 0:00:00
Writing results to: RTY_101.json
```
