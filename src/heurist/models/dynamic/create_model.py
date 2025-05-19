from heurist.models.dynamic.annotation import PydanticField
from heurist.sql.sql_safety import SafeSQLName
from pydantic import BaseModel, Field
from pydantic import create_model as pydantic_create_model


class HeuristRecord:
    def __init__(self, rty_Name: str, rty_ID: int, detail_metadata: list[dict]):
        self.rty_ID = rty_ID
        # Create an SQL-safe name to give the model when it's serialized to a table
        self.table_name = SafeSQLName().create_table_name(record_name=rty_Name)
        # Create the Pydantic model
        self.model = create_record_type_model(
            model_name=self.table_name, detail_metadata=detail_metadata
        )


def create_record_type_model(model_name: str, detail_metadata: list[dict]) -> BaseModel:
    """
    Each detail's set of metadata must be a dictionary with the following keys:
        dty_ID,
        rst_DisplayName,
        dty_Type,
        rst_MaxValues

    Examples:
        >>> d1 = {'dty_ID': 1,
        ... 'rst_DisplayName': 'label',
        ... 'dty_Type': 'enum',
        ... 'rst_MaxValues': 1}
        >>> d2 = {'dty_ID': 2,
        ... 'rst_DisplayName': 'date',
        ... 'dty_Type': 'date',
        ... 'rst_MaxValues': 1}
        >>> model = create_record_type_model('test', [d1, d2])
        >>> model.__annotations__.keys()
        dict_keys(['id', 'type', 'DTY1', 'DTY1_TRM', 'DTY2'])

    Args:
        model_name (str): The model's name.
        detail_metadata (list[dict]): A list of metadata about each field (detail).

    Return:
        (BaseModel): Pydantic model.
    """

    # Indifferent to the record's data fields, set up universal data fields
    # present in every dynamic Pydantic model for records of any type
    kwargs = {
        "id": (
            int,
            Field(
                default=0,
                alias="rec_ID",
                validation_alias="rec_ID",
                serialization_alias="H-ID",
            ),
        ),
        "type": (
            int,
            Field(
                default=0,
                alias="rec_RecTypeID",
                validation_alias="rec_RecTypeID",
                serialization_alias="type_id",
            ),
        ),
    }

    # Convert each of the record's details into a Pydantic kwarg
    for detail in detail_metadata:
        # Add the field's default parsed value
        annotation = PydanticField(**detail)
        field = annotation.build_field()
        kwargs.update(field)

        if detail["dty_Type"] == "enum":
            field = annotation.build_term_fk()
            kwargs.update(field)

    # Using Pydantic's 'create_model' module, build the dynamic model
    return pydantic_create_model(model_name, **kwargs)
