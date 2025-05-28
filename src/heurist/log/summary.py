from collections import Counter

from heurist.log import yield_log_blocks
from rich.table import Table


def log_summary(lines: list[str]) -> tuple[Table, Table]:
    rectypes = []
    recs = []
    for block in yield_log_blocks(lines):
        rectypes.append(block.recType)
        recs.append(block.recID)

    rectype_counter = Counter(rectypes)
    rec_counter = Counter(recs)

    rec_table = Table(
        title="Most problematic records",
        caption="Note: Invalid records are not saved in the DuckDB database.",
    )
    rec_table.add_column("Record ID", style="red")
    rec_table.add_column("Number of problems")
    for rec, count in rec_counter.most_common(10):
        rec_table.add_row(str(rec), str(count))

    type_table = Table(
        title="Types of invalid records",
        caption="Note: Invalid records are not saved in the DuckDB database.",
    )
    type_table.add_column("Record Type", style="red")
    type_table.add_column("Number of records")
    for rec, count in rectype_counter.items():
        type_table.add_row(str(rec), str(count))

    return type_table, rec_table
