QUERY = """
SELECT
	FIRST_VALUE(rst_DisplayName) OVER (PARTITION BY group_id) AS sec,
	FIRST_VALUE(rst_DisplayHelpText) OVER (PARTITION BY group_id) AS secHelpText,
	*
FROM (
        SELECT
            COUNT( 
            	CASE WHEN dty_type LIKE 'separator' THEN rst_DisplayName ELSE NULL end
            ) OVER (ORDER BY rst_DisplayOrder) AS group_id,
            *
        FROM rst
        JOIN rty ON rst_RecTypeID = rty_ID
        JOIN dty ON rst_DetailTypeID = dty_ID
        WHERE rty_ID = ?
)
ORDER BY rst_DisplayOrder
"""
