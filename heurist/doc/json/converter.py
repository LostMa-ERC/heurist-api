import duckdb

from heurist.components.sql_models import output_dicts
from heurist.doc.json.models import DTY, RTY


def convert_rty_description(description: duckdb.DuckDBPyRelation) -> dict:

    rel = description.filter("dty_Type not like 'separator'").order(
        "group_id asc, rst_DisplayOrder asc"
    )

    sections = {}

    for field in output_dicts(rel):
        section_id = field["group_id"]
        section_name = field["sec"]
        if not sections.get(section_id):
            sections.update({section_id: {"sectionName": section_name, "fields": []}})
        field_model = DTY.model_validate(field).model_dump()
        sections[section_id]["fields"].append(field_model)

    section_list = list(sections.values())

    rty_rel = rel.limit(1)
    rty_data = output_dicts(rty_rel)[0]
    rty = RTY.model_validate(rty_data)

    output = {rty.rty_ID: {"metadata": rty.model_dump(), "sections": section_list}}
    return output
