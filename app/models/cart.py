from flask import current_app as app


class Cart:
    def __init__(self, userId, pid, quantity, productName, unitPrice):
        self.userId = userId
        self.pid = pid
        self.quantity = quantity
        self.productName = productName 
        self.unitPrice = unitPrice

    @staticmethod
    def get(userId):
        rows = app.db.execute('''
SELECT Carts.userId, Carts.pid, Carts.quantity, name, unit_price
FROM Carts, Products, Purchases
WHERE Carts.userId = :userId and Carts.pid = Products.id and Carts.userId = Purchases.userId
''',
                              userId=userId)
        return [Cart(*row) for row in rows]
 
