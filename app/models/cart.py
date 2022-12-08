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
SELECT Carts.userId, Carts.pid, Carts.quantity, Products.name, Products.price
FROM Carts, Products
WHERE Carts.userId = :userId and Carts.pid = Products.id
''',
                              userId=userId)
        return [Cart(*row) for row in rows]
 
    @staticmethod
    def add_to_cart(userId, productId, quantity):
        rows = app.db.execute('''
INSERT INTO Carts VALUES (:userId, :productId, :quantity)
''',
                              userId = userId, productId = productId, quantity = quantity)
        return

    @staticmethod
    def add_quantity(userId, productId):
        rows = app.db.execute('''
UPDATE Carts
    SET quantity = quantity + 1
    WHERE userId = :userId and pid = :productId
''',
                              userId=userId, productId = productId)
        return

    @staticmethod
    def remove_quantity(userId, productId):
        rows = app.db.execute('''
UPDATE Carts
    SET quantity = quantity - 1
    WHERE userId = :userId and pid = :productId
''',
                              userId=userId, productId = productId)
        return

    @staticmethod
    def remove_from_cart(userId, productId):
        rows = app.db.execute('''
DELETE FROM Carts
    WHERE userId = :userId AND pid = :productId
''',
                              userId=userId, productId = productId)
        return

    @staticmethod
    def check(userId, productId):
        rows = app.db.execute('''
SELECT *
FROM Carts 
WHERE userId = :userId and pid = :productId
''',
                              userId=userId, productId = productId)
        if rows: 
            return True
        else:
            return False       
                
    @staticmethod
    def getQuantity(userId, productId):
        rows = app.db.execute('''
SELECT quantity
FROM Carts 
WHERE userId = :userId and pid = :productId
''',
                              userId=userId, productId = productId)
        if rows == None: 
            return None
        else:
            return rows[0][0]

    @staticmethod
    def getTotalCost(userId):
        rows = app.db.execute('''
SELECT SUM(lineCost)
FROM 
    (
        SELECT Carts.userId, Carts.quantity*Products.price as lineCost
        FROM Carts, Products
        WHERE Carts.pid = Products.id
     ) as temp  
WHERE userId = :userId
''',
                              userId=userId)
        if rows == None: 
            return None
        else:
            return rows[0][0]

    @staticmethod
    def clearUserCart(userId):
        rows = app.db.execute('''
DELETE FROM Carts
    WHERE userId = :userId 
''',
                              userId=userId)
        return

    @staticmethod
    def getCouponValue(code):
        rows = app.db.execute('''
SELECT percentOff
FROM coupons
WHERE code = :code
''',
                              code=code)
        if rows: 
            return rows[0][0]
        else: 
            return None