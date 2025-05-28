from pathlib import Path

VALIDATION_LOG = Path.cwd().joinpath("validation.log")
VALIDATION_LOG.touch(exist_ok=True)
