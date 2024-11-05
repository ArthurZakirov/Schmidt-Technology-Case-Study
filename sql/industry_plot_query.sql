SELECT
    articles.Industry,
    SUM(orders.order_value)  AS sum_of_order_volume
FROM
    orders
JOIN
    articles ON orders.article_id = articles.article_id
GROUP BY
    articles.Industry
ORDER BY
    sum_of_order_volume DESC;