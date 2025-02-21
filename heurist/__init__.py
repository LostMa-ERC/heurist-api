import logging
from pathlib import Path

from heurist.__version__ import __version__ as VERSION

VERSION

DEFAULT_FORMATTER = logging.Formatter("%(name)s\t%(levelname)-8s\t%(message)s")

LOG_DIR = Path.cwd().joinpath("logs")
LOG_DIR.mkdir(exist_ok=True)

TABLES_LOG = LOG_DIR.joinpath("tables.log.tsv")
DATABASE_LOG = LOG_DIR.joinpath("heurist.db.log")


def setup_logger(
    name,
    filepath: Path,
    level=logging.INFO,
    formatter=DEFAULT_FORMATTER,
    filter: logging.Filter | None = None,
):
    handler = logging.FileHandler(filepath, mode="wt", encoding="utf-8")
    handler.setFormatter(formatter)
    if filter:
        handler.addFilter(filter())

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
