from flask import current_app as app
class Product:
    def __init__(self, id, name, price, available, category, theDescription, quantity, sellerId, theImage):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.category = category
        self.theDescription = theDescription
        self.quantity = quantity
        self.sellerId = sellerId
        self.theImage = theImage
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId, theImage
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId, theImage
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def getOff(available, os):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId, theImage
FROM Products
WHERE available = :available
LIMIT 5
OFFSET :os
''',
                              available=available, os = os)
        return [Product(*row) for row in rows]


    @staticmethod
    def getKExpensive(k):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId, theImage
FROM Products
ORDER BY price DESC
LIMIT :k
''',
                              k=k)
        return [Product(*row) for row in rows]

    @staticmethod
    def getBySeller(sellerId):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId, theImage
FROM Products
WHERE sellerId = :sellerId
ORDER BY price DESC
''',
                              sellerId = sellerId)
        return [Product(*row) for row in rows]


    @staticmethod
    def getInventoryBySeller(sellerId, orderMe):
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, theImage
FROM Products
WHERE sellerId = :sellerId
ORDER BY :orderMe DESC
''',
                              sellerId = sellerId, orderMe = orderMe)
        return [Product(*row) for row in rows]


    @staticmethod
    def add_quantity(id, decrementBy):
        rows = app.db.execute('''
UPDATE Products
    SET quantity = quantity + :decrementBy
    WHERE id = :id
''',
                              id = id, decrementBy=decrementBy)
        return

    @staticmethod
    def decrease_quantity(id, decrementBy):
        rows = app.db.execute('''
UPDATE Products
    SET quantity = quantity - :decrementBy
    WHERE id = :id
''',
                              id = id, decrementBy=decrementBy)
        return

    @staticmethod
    def editInventory(sellerId, id, quantityNew):
        rows = app.db.execute('''
UPDATE Products
    SET quantity = :quantityNew
    WHERE id = :id and sellerId = :sellerId
''',
                              sellerId = sellerId, id = id, quantityNew = quantityNew)
        return

    @staticmethod
    def removeFromInventory(sellerId, id):
        rows = app.db.execute('''
DELETE FROM Products
    WHERE sellerId = :sellerId AND id = :id
''',
                              sellerId=sellerId, id = id)
        return


    @staticmethod
    def getByKeyWord(keyWord, myMax, minRating, category, lim, offset):     

        rows = app.db.execute('''
SELECT id, name, price, available, category, Products.theDescription, quantity, sellerId, theImage
FROM Products
WHERE name ILIKE '%' || :keyWord || '%' AND price <= :myMax and category  = :category AND (Select avg(rating) from ProductReviews WHERE id = pid) >= :minRating
ORDER BY price DESC
LIMIT :lim
Offset :offset
''',
                              keyWord=keyWord, myMax = myMax, minRating = minRating, category = category, lim = lim, offset=offset) 
        return [Product(*row) for row in rows]


    @staticmethod
    def noCat(keyWord, myMax, minRating, lim, offset):     
        rows = app.db.execute('''
SELECT id, name, price, available, category, Products.theDescription, quantity, sellerId, theImage
FROM Products
WHERE name ILIKE '%' || :keyWord || '%' AND price <= :myMax AND (Select avg(rating) from ProductReviews WHERE id = pid) >= :minRating
ORDER BY price DESC
LIMIT :lim
Offset :offset
''',
                              keyWord=keyWord, myMax = myMax, minRating = minRating, lim = lim, offset = offset) 
        return [Product(*row) for row in rows]


    @staticmethod
    def getName(productId):     
        rows = app.db.execute('''
SELECT id, name, price, available, category, Products.theDescription, quantity, sellerId, theImage
FROM Products
WHERE id = :productId
''',
                              productId=productId) 
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def getByName(name):     
        rows = app.db.execute('''
SELECT id, name, price, available, category, Products.theDescription, quantity, sellerId, theImage
FROM Products
WHERE name = :name
''',
                              name=name) 
        return [Product(*row) for row in rows]


    @staticmethod
    def getLimOffset(lim, offset):     
        rows = app.db.execute('''
SELECT id, name, price, available, category, theDescription, quantity, sellerId, theImage
FROM Products
Order By 1
LIMIT :lim
Offset :offset
''',
                              lim=lim, offset=offset) 
        return [Product(*row) for row in rows]


    @staticmethod
    def createProduct(name, description, category, price, quantity, available, sellerId, image):
        try:
            rows = app.db.execute("""
INSERT INTO Products(name, theDescription, category, price, quantity, available, sellerId, theImage)
VALUES(:name, :description, :category, :price, :quantity, :available, :sellerId, :image)
RETURNING id
""",name = name, description = description, category = category, price = price, quantity = quantity, available=available, sellerId = sellerId, image = image)
            id = rows[0][0]
            return Product.get(id)
        except Exception as e:
            return str(e)
     

    @staticmethod
    def purchased(userId):
        rows = app.db.execute('''
SELECT pid
FROM Purchases 
WHERE userId = :userId 
''', userId = userId)
        ret = []
        if rows: 
            for row in rows:
                ret.append(row[0])
            return ret 
        else:
            return None
    
    @staticmethod
    def editProduct(id, name, price, available, category, theDescription, quantity, theImage):
        rows = app.db.execute('''
UPDATE Products 
SET id= :id, name = :name, price = :price, available = :available, category = :category, theDescription = :theDescription, quantity = :quantity, theImage = :theImage
WHERE id = :id
''', id=id, name=name, price=price, available=available, category=category, theDescription=theDescription, quantity=quantity, theImage=theImage)