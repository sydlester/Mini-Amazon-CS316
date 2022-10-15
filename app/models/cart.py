from flask import current_app as app


class Cart:
    def __init__(self, userId, pid, quantity):
        self.userId = userId
        self.pid = pid
        self.quantity = quantity

    @staticmethod
    def get(userId):
        rows = app.db.execute('''
SELECT userId, pid, quantity
FROM Carts
WHERE userId = :userId
''',
                              userId=userId)
        return [Cart(*row) for row in rows]
 
