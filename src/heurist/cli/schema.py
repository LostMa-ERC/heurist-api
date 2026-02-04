"""
CLI command for downloading details about a Heurist database schema.
"""

from heurist.api.credentials import CredentialHandler
from heurist.schema import export_schema


def schema_command(
    credentials: CredentialHandler,
    record_group: list,
    outdir: str,
    output_type: str,
    debugging: bool = False,
):
    export_schema(
        db_name=credentials.get_database(),
        login=credentials.get_login(),
        password=credentials.get_password(),
        outdir=outdir,
        debugging=debugging,
        output_type=output_type,
        record_group=record_group
    )
