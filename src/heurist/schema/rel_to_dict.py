import duckdb
from heurist.schema.models import DTY, RTY
from heurist.utils.rel_to_dict_array import rel_to_dict_array


def convert_rty_description(description: duckdb.DuckDBPyRelation) -> dict:
    """
    Convert the SQL result of the joined record type schema description into \
    a Python dictionary.

    Args:
        description (duckdb.DuckDBPyRelation): Relation from SQL query.

    Returns:
        dict: Dictionary representation of a record's schema.
    """

    rel = description.filter("dty_Type not like 'separator'").order(
        "group_id asc, rst_DisplayOrder asc"
    )

    sections = {}

    for field in rel_to_dict_array(rel):
        section_id = field["group_id"]
        section_name = field["sec"]
        if not sections.get(section_id):
            sections.update({section_id: {"sectionName": section_name, "fields": []}})
        field_model = DTY.model_validate(field).model_dump()
        sections[section_id]["fields"].append(field_model)

    section_list = list(sections.values())

    rty_rel = rel.limit(1)
    rty_data = rel_to_dict_array(rty_rel)[0]
    rty = RTY.model_validate(rty_data)

    output = {rty.rty_ID: {"metadata": rty.model_dump(), "sections": section_list}}
    return output
