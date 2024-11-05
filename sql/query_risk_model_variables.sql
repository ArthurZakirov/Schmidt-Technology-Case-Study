SELECT
	suppliers.supplier_id,
	ROUND(SUM(orders.order_value),0) AS sum_of_order_volume,
    MAX(indices.human_rights_index) AS human_rights_index,
    MAX(indices.enivronmental_risk) AS environmental_risk,
    MAX(suppliers.total_company_revenue) AS total_company_revenue,
	MAX(suppliers.certificates_valid) AS certificates_valid,
    MAX(suppliers.status) as status
FROM
	orders
JOIN 
	suppliers ON suppliers.supplier_id = orders.supplier_id
JOIN
	articles ON  articles.Article_ID = orders.article_id
JOIN
	addresses ON addresses.supplier_id = orders.supplier_id
JOIN
	country_mapping ON country_mapping.country_name = addresses.country
JOIN
	indices ON indices.country_id = country_mapping.country_id
GROUP BY
    orders.supplier_id;