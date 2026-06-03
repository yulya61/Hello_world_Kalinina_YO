UPDATE prices 
SET price = price * 1.05 
WHERE product_id <= 5 AND price < 10000;
SELECT * FROM prices WHERE product_id <= 5 AND price < 10500 ORDER BY product_id, price;