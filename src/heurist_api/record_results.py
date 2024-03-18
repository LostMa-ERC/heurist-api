from lxml import etree

from pydantic import BaseModel


from heurist_api.constants import NAMESPACE


class Record(BaseModel):
    """Records from Heurist database.

    Args:
        BaseModel (_type_): _description_
    """
