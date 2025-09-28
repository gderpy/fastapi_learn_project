SELECT
    users.username,
    users.id,
    profiles_1.first_name,
    profiles_1.last_name,
    profiles_1.bio,
    profiles_1.id AS id_1,
    profiles_1.user_id
FROM
    users
    LEFT OUTER JOIN profiles AS profiles_1 ON users.id = profiles_1.user_id
ORDER BY
    users.id
SELECT
    users.username,
    users.id,
    posts_1.title,
    posts_1.body,
    posts_1.id AS id_1,
    posts_1.user_id
FROM
    users
    LEFT OUTER JOIN posts AS posts_1 ON users.id = posts_1.user_id
ORDER BY
    users.id
SELECT
    users.username,
    users.id
FROM
    users
ORDER BY
    users.id
SELECT
    posts.user_id AS posts_user_id,
    posts.title AS posts_title,
    posts.body AS posts_body,
    posts.id AS posts_id
FROM
    posts
WHERE
    posts.user_id IN (?, ?, ?, ?)

SELECT
    orders.promocode,
    orders.created_at,
    orders.id
FROM
    orders
ORDER BY
    orders.id
SELECT
    orders_1.id AS orders_1_id,
    products.name AS products_name,
    products.description AS products_description,
    products.price AS products_price,
    products.id AS products_id
FROM
    orders AS orders_1
    JOIN order_product_association AS order_product_association_1 ON orders_1.id = order_product_association_1.order_id
    JOIN products ON products.id = order_product_association_1.product_id
WHERE
    orders_1.id IN (1, 2)

SELECT
    orders.promocode,
    orders.created_at,
    orders.id
FROM
    orders
ORDER BY
    orders.id

SELECT
    order_product_association.order_id AS order_product_association_order_id,
    order_product_association.id AS order_product_association_id,
    order_product_association.product_id AS order_product_association_product_id,
    order_product_association.count AS order_product_association_count,
    products_1.name AS products_1_name,
    products_1.description AS products_1_description,
    products_1.price AS products_1_price,
    products_1.id AS products_1_id
FROM
    order_product_association
    LEFT OUTER JOIN products AS products_1 ON products_1.id = order_product_association.product_id
WHERE
    order_product_association.order_id IN (1, 2)