SELECT
    articles.Article,
    orders.supplier_id,
    SUM(orders.order_value)  AS sum_of_order_volume
FROM
    orders
JOIN
    articles on articles.article_id = orders.article_id
GROUP BY
    articles.Article, orders.supplier_id
ORDER BY
    articles.Article, sum_of_order_volume DESC;