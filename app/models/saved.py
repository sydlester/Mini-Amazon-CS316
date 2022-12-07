from flask import current_app as app

class Saved:
    def __init__(self, userId, pid, productName, unitPrice):
        self.userId = userId
        self.pid = pid
        self.productName = productName 
        self.unitPrice = unitPrice

    @staticmethod
    def get(userId):
        rows = app.db.execute('''
SELECT Saved.userId, Saved.pid, Products.name, Products.price
    FROM Saved, Products
    WHERE Saved.userId = :userId and Saved.pid = Products.id
''',
                              userId=userId)
        return [S(*row) for row in rows]

    @staticmethod
    def add_to_saved(userId, productId):
        rows = app.db.execute('''
INSERT INTO Saved VALUES (:userId, :productId)
''',
                              userId = userId, productId = productId)
        return

    @staticmethod
    def remove_from_saved(userId, productId):
        rows = app.db.execute('''
DELETE FROM Saved
    WHERE userId = :userId AND pid = :productId
''',
                              userId=userId, productId = productId)
        return

    @staticmethod
    def check(userId, productId):
        rows = app.db.execute('''
SELECT *
FROM Saved 
WHERE userId = :userId and pid = :productId
''',
                              userId=userId, productId = productId)
        if rows: 
            return True
        else:
            return False  
