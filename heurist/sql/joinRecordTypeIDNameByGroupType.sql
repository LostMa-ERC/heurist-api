SELECT
    rty.rty_ID,
    rty.rty_Name
FROM rty
INNER JOIN rtg ON rty.rty_RecTypeGroupID = rtg.rtg_ID