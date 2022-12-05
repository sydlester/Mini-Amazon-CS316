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
    def getByUser(userId, status):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE userId = :userId and fulfilled = :status
ORDER BY 6 DESC
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

    @staticmethod
    def getByOrder(id):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE id = :id
ORDER BY 3
''', id=id)
        if rows:
            return [Purchase(*row) for row in rows]

    @staticmethod
    def getTotalCost(id):
        rows = app.db.execute('''
SELECT Sum(cost) as total
FROM 
    (
        Select id, unit_price*quantity as cost
        From Purchases
        Where id = :id
    ) as TEMP
''', id = id)
        if rows:
            return rows[0][0]

    @staticmethod
    def getTotalQuantity(id):
        rows = app.db.execute('''
SELECT Sum(quantity) as total
FROM purchases
Where id = :id
''', id = id)
        if rows:
            return rows[0][0]
        else:
            return None

    @staticmethod
    def getBySeller(sellerId, status):
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled
FROM Purchases, Products
WHERE Purchases.pid = products.id and products.sellerId = :sellerId status = :status
ORDER BY 6 DESC
''',
                              sellerId=sellerId, status=status)
        if rows:
            return [Purchase(*row) for row in rows]
        else: 
            return None


    @staticmethod
    def getAllBySeller(sellerId):
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled
FROM Purchases, Products
WHERE Purchases.pid = products.id and products.sellerId = :sellerId
ORDER BY 6 DESC
''',
                              sellerId=sellerId)
        if rows:
            return [Purchase(*row) for row in rows]
        else: 
            return None

    @staticmethod
    def markFulfilled(id, pid, userId):
        try:
            rows = app.db.execute("""
UPDATE Purchases
    SET fulfilled = True, time_fulfilled = CURRENT_TIMESTAMP
    WHERE id = :id and pid = :pid and userId = userId
""", id=id, pid=pid, userId=userId)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            return str(e)