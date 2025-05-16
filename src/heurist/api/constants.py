"""Constant text variables for Heurist API."""

import os

HUMA_NUM_SERVER = "https://heurist.huma-num.fr/heurist"

RECORD_XML_EXPORT_PATH = "/export/xml/flathml.php"

RECORD_JSON_EXPORT_PATH = "/hserv/controller/record_output.php"

STRUCTURE_EXPORT_PATH = "/hserv/structure/export/getDBStructureAsXML.php"

timeout_var = os.environ.get("READTIMEOUT", 10)
if isinstance(timeout_var, str):
    timeout_var = int(timeout_var)

READTIMEOUT = timeout_var

MAX_RETRY = 3
