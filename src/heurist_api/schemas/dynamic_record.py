from typing_extensions import _AnnotatedAlias
from pydantic import (
    model_validator,
    model_serializer,
    create_model,
    Field,
    BaseModel as PydanticBaseModel,
)
from typing import Any, Annotated

from heurist_api.schemas import RecordField
from heurist_api.schemas.utils import HeuristDataType, flatten_record_detail


def create_annotated_fields(fields: list[RecordField]):
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
    def get_model_name(cls):
        instance_repr = repr(cls).split(".")[-1]
        return instance_repr.removesuffix("'>")

    @classmethod
    def get_record_type(cls) -> str:
        name = cls.get_model_name()
        return name.split("_")[-1]

    @classmethod
    def from_payload(cls, model_name, fields):
        context = cls.build_fields(fields=fields)
        return create_model(model_name, __base__=cls, **context)

    @classmethod
    def build_rec_ID_params(cls) -> tuple:
        field = Field(
            alias="rec_ID",
            serialization_alias="H-ID",
            validation_alias="rec_ID",
            default=0,  # cannot be None
        )
        return (int, Annotated[int, field])

    @classmethod
    def build_RecTypeID_params(cls) -> tuple:
        field = Field(
            alias="rec_TypeID",
            serialization_alias="type_id",
            validation_alias="rec_TypeID",
            default=0,  # cannot be None
        )
        return (int, Annotated[int, field])

    @classmethod
    def build_fields(cls, fields: list[Field]):
        rec_ID = cls.build_rec_ID_params()
        rec_TypeID = cls.build_RecTypeID_params()
        context = {"rec_ID": rec_ID, "rec_TypeID": rec_TypeID}
        context.update(create_annotated_fields(fields=fields))
        return context

    @model_validator(mode="before")
    @classmethod
    def format_heurist_json(cls, record: dict):
        formatted_json = {}
        rec_ID = record["rec_ID"]
        record_type_ID = record["rec_RecTypeID"]

        formatted_json.update({"rec_ID": rec_ID, "rec_TypeID": record_type_ID})

        details = record["details"]
        for detail in details:
            key_value_pair = flatten_record_detail(detail)
            if key_value_pair:
                formatted_json.update(key_value_pair)

        return formatted_json

    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        result = {}
        for fieldname, annotation in self.model_fields.items():
            key = annotation.default.__metadata__[0].serialization_alias
            value = getattr(self, fieldname)
            # If the value is the field's Annotated default, make it None
            if isinstance(value, _AnnotatedAlias):
                value = None
            result.update({key: value})
        return result
