\COPY Users FROM '../data/users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM '../data/products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Orders FROM '../data/orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_orderId_seq',
                         (SELECT MAX(orderId)+1 FROM Orders),
                         false);                                           

\COPY Purchases FROM '../data/purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);

\COPY Carts FROM '/../data/carts.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY ProductReviews FROM '../data/productReviews.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY SellerReviews FROM '../data/sellerReviews.csv' WITH DELIMITER ',' NULL '' CSV;

