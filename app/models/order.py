from flask import current_app as app


class Order:
    def __init__(self, orderId, userId, fulfilled, time_purchased):
        self.orderId = orderId
        self.user_id = userId
        self.fulfilled = fulfilled
        self.time_purchased = time_purchased

    @staticmethod
    def get(userId):
        rows = app.db.execute('''
SELECT orderId, userId, fulfilled, time_purchased
FROM Orders
WHERE userId = :userId
''',
                              userId=userId)
        return [Order(*row) for row in rows]
