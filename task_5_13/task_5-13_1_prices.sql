UPDATE prices 
SET price = price * 1.10 
WHERE price < 1000;
SELECT * FROM prices WHERE price < 1100 ORDER BY price;
