from typing_extensions import _AnnotatedAlias
from pydantic import (
    model_validator,
    model_serializer,
    create_model,
    Field,
    BaseModel as PydanticBaseModel,
)
from typing import Any, List, Annotated, Dict, Tuple

from heurist_api.schemas import RecordField
from heurist_api.schemas.utils import HeuristDataType


def create_annotated_fields(fields: List[RecordField]):
    # Initiatlize a dictionary of all of the record's fields
    d = {}

    for field in fields:
        # Convert Heurist's DetailType (dty_Type) to a Pydantic field type
        dtype = HeuristDataType.to_pydantic(field.dty_Type)

        # Create the keyword arguments for the Pydantic Field
        kwargs = {
            "alias": field.dty_Name,
            "serialization_alias": field.fieldname,
            "validation_alias": f"dty_{field.dty_ID}",
        }
        if field.rst_RequirementType != "required":
            kwargs.update({"default": None})
        else:
            kwargs.update({"required": True})

        # Pydantic Fields are defined by a tuple:
        # (<type>, <default value>)
        # Create the tuple
        t = (dtype, Annotated[dtype, Field(**kwargs)])

        # Update the dictionary of the record's fields
        d.update({f"dty_{field.dty_ID}": t})

    # Return a dictionary of the record's fields
    return d


class RecordBaseModel(PydanticBaseModel):
    @classmethod
    def from_payload(cls, model_name, fields):
        context = cls.build_fields(fields=fields)
        return create_model(model_name, __base__=cls, **context)

    @classmethod
    def build_rec_ID_params(cls) -> Tuple:
        kwargs = {
            "alias": "rec_ID",
            "serialization_alias": "rec_ID",
            "validation_alias": "rec_ID",
            "primary_key": True,
            "required": True,
        }
        return (int, Annotated[int, Field(**kwargs)])

    @classmethod
    def build_RecTypeID_params(cls) -> Tuple:
        kwargs = {
            "alias": "rec_TypeID",
            "serialization_alias": "rec_TypeID",
            "validation_alias": "rec_TypeID",
            "required": True,
        }
        return (int, Annotated[int, Field(**kwargs)])

    @classmethod
    def build_fields(cls, fields: List[Field]):
        rec_ID = cls.build_rec_ID_params()
        rec_TypeID = cls.build_RecTypeID_params()
        context = create_annotated_fields(fields=fields)
        context.update({"rec_ID": rec_ID, "rec_TypeID": rec_TypeID})
        return context

    @model_validator(mode="before")
    @classmethod
    def format_heurist_json(cls, record: Dict):
        formatted_json = {}
        rec_ID = record["rec_ID"]
        record_type_ID = record["rec_RecTypeID"]
        formatted_json.update({"rec_ID": rec_ID, "rec_TypeID": record_type_ID})

        details = record["details"]
        for detail in details:
            key = f"dty_{detail['dty_ID']}"
            value = detail["value"]
            if not isinstance(value, Dict):
                formatted_json.update({key: value})
        return formatted_json

    @model_serializer
    def ser_model(self) -> Dict[str, Any]:
        result = {}
        for fieldname, annotation in self.model_fields.items():
            value = getattr(self, fieldname)
            if isinstance(value, _AnnotatedAlias):
                value = None
            key = annotation.default.__metadata__[0].serialization_alias
            result.update({key: value})
        return result
