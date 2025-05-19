from pathlib import Path

file_path_record_type_schema = Path(__file__).parent.joinpath(
    "selectRecordTypeSchema.sql"
)
file_path_record_type_metadata_by_group_type = Path(__file__).parent.joinpath(
    "joinRecordTypeIDNameByGroupType.sql"
)
file_path_fully_joined_record_type_metadata = Path(__file__).parent.joinpath(
    "joinRecordTypeMetadata.sql"
)


with open(file_path_record_type_schema) as f:
    RECORD_TYPE_SCHEMA = f.read()

with open(file_path_record_type_metadata_by_group_type) as f:
    RECORD_BY_GROUP_TYPE = f.read()

with open(file_path_fully_joined_record_type_metadata) as f:
    RECORD_TYPE_METADATA = f.read()
