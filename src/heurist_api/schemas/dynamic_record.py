from pydantic import create_model, Field
from typing import List, Annotated

from heurist_api.schemas import RecordField
from heurist_api.schemas.utils import HeuristDataType


def create_fields(fields: List[RecordField]):
    # Initiatlize a dictionary of all of the record's fields
    d = {}

    for field in fields:
        # Convert Heurist's DetailType (dty_Type) to a Pydantic field type
        dtype = HeuristDataType.to_pydantic(field.dty_Type)

        # Create the keyword arguments for the Pydantic Field
        kwargs = {"alias": field.fieldname, "serialization_alias": field.dty_ID}
        if field.rst_RequirementType != "required":
            kwargs.update({"default": None})
        else:
            kwargs.update({"required": True})

        # Pydantic Fields are defined by a tuple:
        # (<type>, <default value>)
        # Create the tuple
        t = (dtype, Annotated[dtype, Field(**kwargs)])

        # Update the dictionary of the record's fields
        d.update({field.dty_Name: t})

    # Return a dictionary of the record's fields
    return d


def create_record_model(fields: List[RecordField]):
    # Parse the record's fields
    dynamic_fields = create_fields(fields=fields)

    # Create a Pydantic Model with the record's type ID and parsed fields
    Record = create_model(
        "Record",
        record_type_id=(int, Field(default=fields[0].rty_ID, frozen=True)),
        **dynamic_fields
    )

    # Return an uninstantiated class of the new Pydantic Model
    return Record
