# Heurist API constants

# pylint: disable=missing-module-docstring


NAMESPACE = {"hml": "https://heuristnetwork.org"}

HEURIST_SERVER = "https://heurist.huma-num.fr/heurist"

RECORD_XML_EXPORT_PATH = "/export/xml/flathml.php"

RECORD_JSON_EXPORT_PATH = "/hserv/controller/record_output.php"

STRUCTURE_EXPORT_PATH = "/hserv/structure/export/getDBStructureAsXML.php"

JOIN_RECORD_STRUCTURES_AND_DETAIL_TYPES = """
SELECT
    rst.rst_RecTypeID,
    dty.dty_ID,
    dty.dty_Name,
    rst.rst_RequirementType,
	dty.dty_Type
FROM main.record_structures rst
JOIN main.detail_types dty ON dty.dty_ID = rst.rst_DetailTypeID
WHERE dty.dty_Type NOT LIKE 'separator'
AND dty.dty_TYPE NOT LIKE 'relmarker'
ORDER BY rst.rst_DisplayOrder
"""

JOIN_RECORD_TYPE_WITH_STRUCTURE = """
SELECT
    rty.rty_Name,
    *
FROM {}
JOIN main.record_types AS rty ON rst_RecTypeID = rty.rty_ID
WHERE rty.rty_ID = '{}'
"""


EXAMPLE_XML = b"<xml>\
<RecTypes>\
    <rty>\
        <rty_ID>102</rty_ID>\
        <rty_Name>cycle</rty_Name>\
        <rty_OrderInGroup>0</rty_OrderInGroup>\
        <rty_Description>A grouping of works, themselves instantiated as texts; e.g. the cycle des Lorrains, represented as texts by the songs of Garin, Hervis, Or the Avengers, if you like comic books.</rty_Description>\
        <rty_TitleMask>[2-1]</rty_TitleMask>\
        <rty_CanonicalTitleMask>160</rty_CanonicalTitleMask>\
        <rty_Plural>cycles</rty_Plural>\
        <rty_Status>open</rty_Status>\
        <rty_OriginatingDBID>0</rty_OriginatingDBID>\
        <rty_NameInOriginatingDB>Cycle</rty_NameInOriginatingDB>\
        <rty_IDInOriginatingDB>102</rty_IDInOriginatingDB>\
        <rty_NonOwnerVisibility>viewable</rty_NonOwnerVisibility>\
        <rty_ShowInLists>1</rty_ShowInLists>\
        <rty_RecTypeGroupID>23</rty_RecTypeGroupID>\
        <rty_RecTypeModelIDs/>\
        <rty_FlagAsFieldset>0</rty_FlagAsFieldset>\
        <rty_ReferenceURL/>\
        <rty_AlternativeRecEditor/>\
        <rty_Type>normal</rty_Type>\
        <rty_ShowURLOnEditForm>0</rty_ShowURLOnEditForm>\
        <rty_ShowDescriptionOnEditForm>1</rty_ShowDescriptionOnEditForm>\
        <rty_Modified>2022-09-03 15:39:36</rty_Modified>\
        <rty_LocallyModified>0</rty_LocallyModified>\
    </rty>\
</RecTypes>\
<RecStructure>\
    <rst>\
        <rst_ID>3327</rst_ID>\
        <rst_RecTypeID>102</rst_RecTypeID>\
        <rst_DetailTypeID>57</rst_DetailTypeID>\
        <rst_DisplayName>Identification</rst_DisplayName>\
        <rst_DisplayHelpText> </rst_DisplayHelpText>\
        <rst_DisplayExtendedDescription/>\
        <rst_DisplayOrder>000</rst_DisplayOrder>\
        <rst_DisplayWidth>100</rst_DisplayWidth>\
        <rst_DisplayHeight>3</rst_DisplayHeight>\
        <rst_DefaultValue>tabs</rst_DefaultValue>\
        <rst_RecordMatchOrder>0</rst_RecordMatchOrder>\
        <rst_CalcFunctionID/>\
        <rst_CalcFieldMask/>\
        <rst_RequirementType>recommended</rst_RequirementType>\
        <rst_NonOwnerVisibility>public</rst_NonOwnerVisibility>\
        <rst_Status>open</rst_Status>\
        <rst_MayModify>open</rst_MayModify>\
        <rst_OriginatingDBID>0</rst_OriginatingDBID>\
        <rst_IDInOriginatingDB/>\
        <rst_MaxValues>1</rst_MaxValues>\
        <rst_MinValues>0</rst_MinValues>\
        <rst_InitialRepeats>1</rst_InitialRepeats>\
        <rst_DisplayDetailTypeGroupID/>\
        <rst_FilteredJsonTermIDTree/>\
        <rst_PtrFilteredIDs/>\
        <rst_CreateChildIfRecPtr>0</rst_CreateChildIfRecPtr>\
        <rst_PointerMode>dropdown_add</rst_PointerMode>\
        <rst_PointerBrowseFilter/>\
        <rst_OrderForThumbnailGeneration/>\
        <rst_TermIDTreeNonSelectableIDs/>\
        <rst_ShowDetailCertainty>0</rst_ShowDetailCertainty>\
        <rst_ShowDetailAnnotation>0</rst_ShowDetailAnnotation>\
        <rst_NumericLargestValueUsed/>\
        <rst_EntryMask/>\
        <rst_Modified>2023-01-05 14:03:52</rst_Modified>\
        <rst_LocallyModified>0</rst_LocallyModified>\
        <rst_SemanticReferenceURL/>\
        <rst_TermsAsButtons>0</rst_TermsAsButtons>\
    </rst>\
    <rst>\
        <rst_ID>3328</rst_ID>\
        <rst_RecTypeID>102</rst_RecTypeID>\
        <rst_DetailTypeID>1</rst_DetailTypeID>\
        <rst_DisplayName>Title</rst_DisplayName>\
        <rst_DisplayHelpText>Titre du cycle</rst_DisplayHelpText>\
        <rst_DisplayExtendedDescription/>\
        <rst_DisplayOrder>001</rst_DisplayOrder>\
        <rst_DisplayWidth>40</rst_DisplayWidth>\
        <rst_DisplayHeight>3</rst_DisplayHeight>\
        <rst_DefaultValue/>\
        <rst_RecordMatchOrder>0</rst_RecordMatchOrder>\
        <rst_CalcFunctionID/>\
        <rst_CalcFieldMask/>\
        <rst_RequirementType>optional</rst_RequirementType>\
        <rst_NonOwnerVisibility>public</rst_NonOwnerVisibility>\
        <rst_Status>open</rst_Status>\
        <rst_MayModify>open</rst_MayModify>\
        <rst_OriginatingDBID>0</rst_OriginatingDBID>\
        <rst_IDInOriginatingDB/>\
        <rst_MaxValues>1</rst_MaxValues>\
        <rst_MinValues>0</rst_MinValues>\
        <rst_InitialRepeats>1</rst_InitialRepeats>\
        <rst_DisplayDetailTypeGroupID/>\
        <rst_FilteredJsonTermIDTree/>\
        <rst_PtrFilteredIDs/>\
        <rst_CreateChildIfRecPtr>0</rst_CreateChildIfRecPtr>\
        <rst_PointerMode>dropdown_add</rst_PointerMode>\
        <rst_PointerBrowseFilter/>\
        <rst_OrderForThumbnailGeneration/>\
        <rst_TermIDTreeNonSelectableIDs/>\
        <rst_ShowDetailCertainty>0</rst_ShowDetailCertainty>\
        <rst_ShowDetailAnnotation>0</rst_ShowDetailAnnotation>\
        <rst_NumericLargestValueUsed/>\
        <rst_EntryMask/>\
        <rst_Modified>2023-01-05 14:03:52</rst_Modified>\
        <rst_LocallyModified>0</rst_LocallyModified>\
        <rst_SemanticReferenceURL/>\
        <rst_TermsAsButtons>0</rst_TermsAsButtons>\
    </rst>\
    <rst>\
        <rst_ID>3463</rst_ID>\
        <rst_RecTypeID>102</rst_RecTypeID>\
        <rst_DetailTypeID>1179</rst_DetailTypeID>\
        <rst_DisplayName>Related Cycle</rst_DisplayName>\
        <rst_DisplayHelpText>Cycle of which this cycle is a part.</rst_DisplayHelpText>\
        <rst_DisplayExtendedDescription/>\
        <rst_DisplayOrder>002</rst_DisplayOrder>\
        <rst_DisplayWidth>100</rst_DisplayWidth>\
        <rst_DisplayHeight>3</rst_DisplayHeight>\
        <rst_DefaultValue/>\
        <rst_RecordMatchOrder>0</rst_RecordMatchOrder>\
        <rst_CalcFunctionID/>\
        <rst_CalcFieldMask/>\
        <rst_RequirementType>recommended</rst_RequirementType>\
        <rst_NonOwnerVisibility>public</rst_NonOwnerVisibility>\
        <rst_Status>open</rst_Status>\
        <rst_MayModify>open</rst_MayModify>\
        <rst_OriginatingDBID>0</rst_OriginatingDBID>\
        <rst_IDInOriginatingDB/>\
        <rst_MaxValues>1</rst_MaxValues>\
        <rst_MinValues>0</rst_MinValues>\
        <rst_InitialRepeats>1</rst_InitialRepeats>\
        <rst_DisplayDetailTypeGroupID/>\
        <rst_FilteredJsonTermIDTree/>\
        <rst_PtrFilteredIDs/>\
        <rst_CreateChildIfRecPtr>0</rst_CreateChildIfRecPtr>\
        <rst_PointerMode>dropdown_add</rst_PointerMode>\
        <rst_PointerBrowseFilter/>\
        <rst_OrderForThumbnailGeneration/>\
        <rst_TermIDTreeNonSelectableIDs/>\
        <rst_ShowDetailCertainty>0</rst_ShowDetailCertainty>\
        <rst_ShowDetailAnnotation>0</rst_ShowDetailAnnotation>\
        <rst_NumericLargestValueUsed/>\
        <rst_EntryMask/>\
        <rst_Modified>2024-03-27 13:39:21</rst_Modified>\
        <rst_LocallyModified>0</rst_LocallyModified>\
        <rst_SemanticReferenceURL/>\
        <rst_TermsAsButtons>0</rst_TermsAsButtons>\
    </rst>\
</RecStructure>\
<DetailTypes>\
    <dty>\
        <dty_ID>1</dty_ID>\
        <dty_Name>Name or Title (please rename appropriately)</dty_Name>\
        <dty_Documentation>\Name or phrase used to identify the represented object/entity\</dty_Documentation>\
        <dty_Type>freetext</dty_Type>\
        <dty_HelpText>\The main name or title for the object. Title of a work, family name of person, name of organisation etc.\</dty_HelpText>\
        <dty_ExtendedDescription/>\
        <dty_EntryMask/>\
        <dty_Status>reserved</dty_Status>\
        <dty_OriginatingDBID>2</dty_OriginatingDBID>\
        <dty_NameInOriginatingDB>Name</dty_NameInOriginatingDB>\
        <dty_IDInOriginatingDB>1</dty_IDInOriginatingDB>\
        <dty_DetailTypeGroupID>1</dty_DetailTypeGroupID>\
        <dty_OrderInGroup>0</dty_OrderInGroup>\
        <dty_JsonTermIDTree/>\
        <dty_TermIDTreeNonSelectableIDs/>\
        <dty_PtrTargetRectypeIDs/>\
        <dty_FieldSetRectypeID>0</dty_FieldSetRectypeID>\
        <dty_ShowInLists>1</dty_ShowInLists>\
        <dty_NonOwnerVisibility>viewable</dty_NonOwnerVisibility>\
        <dty_Modified>2021-12-31 04:41:59</dty_Modified>\
        <dty_LocallyModified>1</dty_LocallyModified>\
        <dty_SemanticReferenceURL/>\
    </dty>\
    <dty>\
        <dty_ID>57</dty_ID>\
        <dty_Name>Header 1</dty_Name>\
        <dty_Documentation>\Please document the nature of this detail type (field)) ...\</dty_Documentation>\
        <dty_Type>separator</dty_Type>\
        <dty_HelpText> </dty_HelpText>\
        <dty_ExtendedDescription/>\
        <dty_EntryMask/>\
        <dty_Status>open</dty_Status>\
        <dty_OriginatingDBID>2</dty_OriginatingDBID>\
        <dty_NameInOriginatingDB>Header 1</dty_NameInOriginatingDB>\
        <dty_IDInOriginatingDB>57</dty_IDInOriginatingDB>\
        <dty_DetailTypeGroupID>139</dty_DetailTypeGroupID>\
        <dty_OrderInGroup>0</dty_OrderInGroup>\
        <dty_JsonTermIDTree/>\
        <dty_TermIDTreeNonSelectableIDs/>\
        <dty_PtrTargetRectypeIDs/>\
        <dty_FieldSetRectypeID>0</dty_FieldSetRectypeID>\
        <dty_ShowInLists>0</dty_ShowInLists>\
        <dty_NonOwnerVisibility>viewable</dty_NonOwnerVisibility>\
        <dty_Modified>2021-12-31 05:59:44</dty_Modified>\
        <dty_LocallyModified>1</dty_LocallyModified>\
        <dty_SemanticReferenceURL/>\
    </dty>\
    <dty>\
        <dty_ID>1179</dty_ID>\
        <dty_Name>Related Cycle</dty_Name>\
        <dty_Documentation>\Please document the nature of this detail type (field)) ...\</dty_Documentation>\
        <dty_Type>relmarker</dty_Type>\
        <dty_HelpText>Cycle of which this cycle is a part.</dty_HelpText>\
        <dty_ExtendedDescription/>\
        <dty_EntryMask/>\
        <dty_Status>open</dty_Status>\
        <dty_OriginatingDBID>0</dty_OriginatingDBID>\
        <dty_NameInOriginatingDB>Related Cycle</dty_NameInOriginatingDB>\
        <dty_IDInOriginatingDB>1179</dty_IDInOriginatingDB>\
        <dty_DetailTypeGroupID>1</dty_DetailTypeGroupID>\
        <dty_OrderInGroup>0</dty_OrderInGroup>\
        <dty_JsonTermIDTree>3001</dty_JsonTermIDTree>\
        <dty_TermIDTreeNonSelectableIDs/>\
        <dty_PtrTargetRectypeIDs>102</dty_PtrTargetRectypeIDs>\
        <dty_FieldSetRectypeID/>\
        <dty_ShowInLists>1</dty_ShowInLists>\
        <dty_NonOwnerVisibility>viewable</dty_NonOwnerVisibility>\
        <dty_Modified>2024-03-27 13:39:21</dty_Modified>\
        <dty_LocallyModified>0</dty_LocallyModified>\
        <dty_SemanticReferenceURL/>\
    </dty>\
</DetailTypes>\
</xml>"
