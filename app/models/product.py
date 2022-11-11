from flask import current_app as app

class Product:
    def __init__(self, id, name, price, available, category, theDescription, quantity, sellerId):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.category = category
        self.theDescription = theDescription
        self.quantity = quantity
        self.sellerId = sellerId

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
    

    @staticmethod
    def getKExpensive(k):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId
FROM Products
ORDER BY price DESC
LIMIT :k
''',
                              k=k)
        return [Product(*row) for row in rows]

    @staticmethod
    def getBySeller(sellerId):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId
FROM Products
WHERE sellerId = :sellerId
ORDER BY price DESC
''',
                              sellerId = sellerId)
        return [Product(*row) for row in rows]


    @staticmethod
    def getInventoryBySeller(sellerId, orderMe):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity
FROM Products
WHERE sellerId = :sellerId
ORDER BY :orderMe DESC
''',
                              sellerId = sellerId, orderMe = orderMe)
        return [Product(*row) for row in rows]


    @staticmethod
    def add_quantity(sellerId, id):
        rows = app.db.execute('''
UPDATE Products
    SET quantity = quantity + 1
    WHERE sellerId = :sellerId and id = :id
''',
                              sellerId=sellerId, id = id)
        return

    @staticmethod
    def decrease_quantity(sellerId, id):
        rows = app.db.execute('''
UPDATE Products
    SET quantity = quantity - 1
    WHERE sellerId = :sellerId and id = :id
''',
                              sellerId=sellerId, id = id)
        return

    @staticmethod
    def removeFromInventory(sellerId, id):
        rows = app.db.execute('''
DELETE FROM Products
    WHERE sellerId = :sellerId AND id = :id
''',
                              sellerId=sellerId, id = id)
        return
