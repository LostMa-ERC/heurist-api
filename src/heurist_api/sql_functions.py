from dataclasses import dataclass
from duckdb import DuckDBPyConnection


DROP_FUNCTION = "DROP FUNCTION IF EXISTS {}"


INNER_REGEX = "regexp_replace(s, '\(.+\)', '')"
MIDDLE_REGEX = f"regexp_replace({INNER_REGEX}, '\W', '_')"
OUTTER_REGEX = f"regexp_replace({MIDDLE_REGEX}, '/', '_')"
ANOTHER_REGEX = f"replace({OUTTER_REGEX}, ' ', '_')"
REGEX = f"regexp_replace({ANOTHER_REGEX}, '_+', '_')"
TRIM = f"trim({REGEX}, '_')"


@dataclass
class SQLSafeFunction:
    name: str = "sql_safe_name"
    drop_stmt: str = DROP_FUNCTION.format(name)
    create_stmt: str = f"""
CREATE FUNCTION {name} (s, i) as concat('dty_', i, '_', lower({TRIM}))
    """

    @classmethod
    def drop(cls, conn: DuckDBPyConnection):
        conn.sql(cls.drop_stmt)

    @classmethod
    def create(cls, conn: DuckDBPyConnection):
        conn.sql(cls.create_stmt)


@dataclass
class ConvertReqFunction:
    name: str = "convert_requirement"
    drop_stmt: str = DROP_FUNCTION.format(name)
    create_stmt: str = f"""
CREATE FUNCTION {name} (s) as case when s = 'required' then 'NOT NULL' else NULL end
"""

    @classmethod
    def drop(cls, conn: DuckDBPyConnection):
        conn.sql(cls.drop_stmt)

    @classmethod
    def create(cls, conn: DuckDBPyConnection):
        conn.sql(cls.drop_stmt)
        conn.sql(cls.create_stmt)
