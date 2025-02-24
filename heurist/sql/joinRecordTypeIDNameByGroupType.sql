/* Select the ID and name of record types that are in
targeted record type groups.

This query should be appended with 1 or more conditions
of "rtg.rtg_Name" = '<target group name>'. */
SELECT
    rty.rty_ID,
    rty.rty_Name
FROM rty
INNER JOIN rtg ON rty.rty_RecTypeGroupID = rtg.rtg_ID