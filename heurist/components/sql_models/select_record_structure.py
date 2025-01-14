QUERY = """
SELECT
	FIRST_VALUE(rst_DisplayName) OVER (PARTITION BY group_id) AS sec,
	FIRST_VALUE(rst_DisplayHelpText) OVER (PARTITION BY group_id) AS secHelpText,
	*
FROM (
SELECT *
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
	LEFT JOIN (
		SELECT 
				a.vocab_id as trm_TreeID,
				b.trm_Label,
				b.trm_Description,
				a.term_count as n_vocabTerms,
				a.terms as vocabTerms
			FROM (
			SELECT
				trm_ParentTermID AS vocab_id,
				count(*) AS term_count, 
				map(list(trm_Label), list({"description": trm_Description, "url": trm_SemanticReferenceURL, "id": trm_ID})) AS terms
			FROM trm
			GROUP BY trm_ParentTermID
			) a
			LEFT JOIN trm b ON a.vocab_id = b.trm_ID
	) c ON c.trm_TreeID = dty_JsonTermIDTree
    ORDER BY rst_DisplayOrder
)
ORDER BY rst_DisplayOrder
"""
