from flask import current_app as app

class Purchase:
    def __init__(self, id, userId, pid, quantity, unit_price, time_ordered, fulfilled, time_fulfilled):
        self.id = id
        self.userId = userId
        self.pid = pid
        self.quantity = quantity
        self.unit_price = unit_price
        self.time_ordered = time_ordered
        self.fulfilled = fulfilled
        self.time_fulfilled = time_fulfilled

    @staticmethod
    def get(userId, status):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE userId = :userId and fulfilled = :status
''',
                              userId=userId, status=status)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def createPurchase(id, userId, pid, quantity, unit_price, time_ordered, fulfilled, time_fulfilled):
        try:
            rows = app.db.execute("""
INSERT INTO Purchases(id, userId, pid, quantity, unit_price, time_ordered, fulfilled, time_fulfilled)
VALUES(:id, :userId, :pid, :quantity, :unit_price, :time_ordered, :fulfilled, :time_fulfilled)
""",id = id, userId=userId, pid = pid, quantity = quantity, unit_price = unit_price, time_ordered = time_ordered, fulfilled=fulfilled, time_fulfilled = time_fulfilled)
            id = rows[0][0]
            return Purchase.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            return str(e)

    @staticmethod
    def getMax():
        rows = app.db.execute('''
SELECT max(id)
FROM Purchases
''',)
        if rows:
            return rows[0][0]