SELECT
	orders.supplier_id AS supplier_id,
	SUM(orders.order_value)  AS sum_of_order_volume,
    MAX(addresses.country) AS country,
    MAX(articles.Industry) AS Industry
FROM
	orders
JOIN 
	suppliers ON suppliers.supplier_id = orders.supplier_id
JOIN
	articles ON  articles.Article_ID = orders.article_id
JOIN
	addresses ON addresses.supplier_id = orders.supplier_id
GROUP BY
	orders.supplier_id;