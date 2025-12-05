-- 1 --
SELECT * FROM customer WHERE town LIKE 'h%';

-- 2 --
SELECT * FROM item WHERE cost_price IS NULL OR sell_price IS NULL;

-- 3 --
SELECT customer_id, title, fname, lname, addressline, town, zipcode, phone FROM customer;

-- 4 --
SELECT CONCAT_WS(' ', customer_id, title, fname, lname, addressline, town, zipcode, phone) AS customer_info FROM customer;

-- 5 --
SELECT
    o.orderinfo_id,
    c.fname,
    c.lname,
    o.date_placed,
    i.description,
    ol.quantity
FROM orderinfo o
JOIN customer c ON o.customer_id = c.customer_id
JOIN orderline ol ON o.orderinfo_id = ol.orderinfo_id
JOIN item i ON ol.item_id = i.item_id
ORDER BY o.orderinfo_id;

-- 6 --
SELECT
    o.orderinfo_id,
    c.fname,
    c.lname,
    o.date_placed,
    i.description,
    SUM(ol.quantity * i.sell_price) AS total_value
FROM orderinfo o
JOIN customer c ON o.customer_id = c.customer_id
JOIN orderline ol ON o.orderinfo_id = ol.orderinfo_id
JOIN item i ON ol.item_id = i.item_id
GROUP BY o.orderinfo_id, c.fname, c.lname, o.date_placed, i.description
ORDER BY o.orderinfo_id;

-- 7 --
SELECT
    o.orderinfo_id,
    c.fname,
    c.lname,
    o.date_placed,
    i.description,
    ol.quantity
FROM orderinfo o
JOIN customer c ON o.customer_id = c.customer_id
JOIN orderline ol ON o.orderinfo_id = ol.orderinfo_id
JOIN item i ON ol.item_id = i.item_id
WHERE c.fname = 'Ann' AND c.lname = 'Stones'
ORDER BY o.orderinfo_id;
