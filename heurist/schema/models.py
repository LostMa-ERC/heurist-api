from typing import List, Optional

from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


def convert_vocab_map_to_list(vocab_map: dict | None) -> list[dict]:
    """
    Convert map generated in the SQL query to a list of vocab dictionary objects.

    See the SQL query in the sql/ directory. The relevant selection is:
        map(list(trm_Label), list(
            {
                "description": trm_Description,
                "url": trm_SemanticReferenceURL,
                "id": trm_ID
            })
        ) AS terms

    Examples:
        >>> vocab0 = {'perg': {'description': 'Parchment', 'url': None, 'id': 9782}}
        >>> vocab1 = {'chart': {'description': 'Paper', 'url': None, 'id': 9783}}
        >>> vocab2 = {'mixed': {'description': None, 'url': None, 'id': 9785}}
        >>> map = vocab0 | vocab1 | vocab2
        >>> terms = convert_vocab_map_to_list(map)
        >>> len(terms)
        3
        >>> terms[0]
        {'label': 'perg', 'description': 'Parchment', 'url': None, 'id': 9782}

    Args:
        vocab_map (dict | None): Map created in SQL query from aggregation function.

    Returns:
        list[dict]: List of vocabulary term metadata in dictionary objects.
    """

    vocab_terms = []
    if vocab_map:
        for k, v in vocab_map.items():
            nd = {"label": k} | v
            vocab_terms.append(nd)
    return vocab_terms


VocabTerms = Annotated[list, BeforeValidator(convert_vocab_map_to_list)]


class DTY(BaseModel):
    rst_DisplayName: str
    rst_DisplayHelpText: str
    dty_ID: int
    dty_Type: str
    dty_PtrTargetRectypeIDs: Optional[List[int]]
    dty_SemanticReferenceURL: Optional[str]
    trm_TreeID: Optional[int]
    trm_Label: Optional[str]
    trm_Description: Optional[str]
    rst_RequirementType: str
    rst_MaxValues: int
    vocabTerms: Optional[VocabTerms]


class RTY(BaseModel):
    rty_ID: int
    rty_Name: str
    rty_Description: str
    rty_TitleMask: str
    rty_ReferenceURL: Optional[str]
