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
                        
\COPY Purchases FROM '../data/purchases.csv' WITH DELIMITER ',' NULL '' CSV                                    

\COPY Carts FROM '../data/carts.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY ProductReviews FROM '../data/productReviews.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY SellerReviews FROM '../data/sellerReviews.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Messages FROM '../data/messages.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.messages_id_seq',
                         (SELECT MAX(id)+1 FROM Messages),
                         false);

\COPY FulFilledPurchases FROM '../data/fulfilledPurchases.csv' WITH DELIMITER ',' NULL '' CSV;
