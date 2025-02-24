SELECT
    dty_ID,
    rst_DisplayName,
    dty_Type,
    rst_MaxValues
FROM rst
INNER JOIN rty ON rst.rst_RecTypeID = rty.rty_ID
INNER JOIN dty ON rst.rst_DetailTypeID = dty.dty_ID
WHERE rty.rty_ID = ?
AND dty.dty_Type NOT LIKE 'separator'
AND dty.dty_Type NOT LIKE 'relmarker'
ORDER BY rst.rst_DisplayOrder