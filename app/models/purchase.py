from flask import current_app as app

class Purchase:
    def __init__(self, id, orderId, userId, pid, quantity, unit_price):
        self.id = id
        self.orderId = orderId
        self.userId = userId
        self.pid = pid
        self.quantity = quantity
        self.unit_price = unit_price

    @staticmethod
    def get(userId):
        rows = app.db.execute('''
SELECT id, orderId, userId, pid, quantity, unit_price
FROM Purchases
WHERE userId = :userId
''',
                              userId=userId)
        return [Purchase(*row) for row in rows]
