from flask import current_app as app

class Purchase:
    def __init__(self, id, userId, pid, quantity, unit_price, time_ordered, fulfilled, time_fulfilled, discountAmount):
        self.id = id
        self.userId = userId
        self.pid = pid
        self.quantity = quantity
        self.unit_price = unit_price
        self.time_ordered = time_ordered
        self.fulfilled = fulfilled
        self.time_fulfilled = time_fulfilled
        self.discountAmount=discountAmount

    @staticmethod
    def getByUser(userId):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE userId = :userId
ORDER BY 6 DESC
''',
                              userId=userId)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def createPurchase(id, userId, pid, quantity, unit_price, time_ordered, fulfilled, time_fulfilled, discountAmount):
        try:
            rows = app.db.execute("""
INSERT INTO Purchases(id, userId, pid, quantity, unit_price, time_ordered, fulfilled, time_fulfilled, discountAmount)
VALUES(:id, :userId, :pid, :quantity, :unit_price, :time_ordered, :fulfilled, :time_fulfilled, :discountAmount)
""",id = id, userId=userId, pid = pid, quantity = quantity, unit_price = unit_price, time_ordered = time_ordered, fulfilled=fulfilled, time_fulfilled = time_fulfilled, discountAmount=discountAmount)
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
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
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
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
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
    
    @staticmethod
    def getTotalCostSeller(id, sellerId):
        rows = app.db.execute('''
SELECT Sum(cost) as total
FROM 
    (
        Select Purchases.id, unit_price*Purchases.quantity as cost
        From Purchases, products
        Where Purchases.id = :id and sellerId = :sellerId and purchases.pid = products.id 
    ) as TEMP
''', id=id, sellerId=sellerId)
        if rows:
            return rows[0][0]
    
    @staticmethod
    def getTotalQuantitySeller(id, sellerId):
        rows = app.db.execute('''
SELECT Sum(Purchases.quantity) as total
FROM Purchases, Products
WHERE Purchases.id = :id and sellerId = :sellerId and purchases.pid = products.id 
''', id=id, sellerId=sellerId)
        if rows:
            return rows[0][0]
    

    @staticmethod
    def getByOrderSeller(id, sellerId):
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.id = :id and sellerId = :sellerId and Products.id = Purchases.pid
ORDER BY 3
''', id=id, sellerId = sellerId)
        if rows:
            return [Purchase(*row) for row in rows]
    

    @staticmethod
    def getBySellerKeyWord(keyWord, sellerId):     
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.pid = Products.id and sellerId = :sellerId and name ILIKE '%' || :keyWord || '%' 
ORDER BY time_ordered DESC
''',
                              keyWord=keyWord, sellerId = sellerId) 
        return [Purchase(*row) for row in rows]

        getBySellerKeyWordBuyerId

    @staticmethod
    def getBySellerKeyWordBuyerId(keyWord, buyerId, sellerId):     
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.pid = Products.id and Purchases.userId = :buyerId and sellerId = :sellerId and name ILIKE '%' || :keyWord || '%' 
ORDER BY time_ordered DESC
''',
                              keyWord=keyWord, sellerId = sellerId, buyerId = buyerId) 
        return [Purchase(*row) for row in rows]

    @staticmethod
    def getBySellerKeyWordDate(keyWord, sellerId, year, month, day):     
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.pid = Products.id and extract(year from time_ordered) = :year and extract(month from time_ordered) = :month and extract(day from time_ordered) = :day and sellerId = :sellerId and name ILIKE '%' || :keyWord || '%' 
ORDER BY time_ordered DESC
''',
                              keyWord=keyWord, sellerId=sellerId,year=year, month=month, day=day) 
        return [Purchase(*row) for row in rows]


    @staticmethod
    def getBySellerKeyWordBuyerIdDate(keyWord, sellerId, buyerId, year, month, day):     
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.pid = Products.id and userId = :buyerId and extract(year from time_ordered) = :year and extract(month from time_ordered) = :month and extract(day from time_ordered) = :day and sellerId = :sellerId and name ILIKE '%' || :keyWord || '%' 
ORDER BY time_ordered DESC
''',
                              keyWord=keyWord, sellerId=sellerId, buyerId = buyerId, year=year, month=month, day=day) 
        return [Purchase(*row) for row in rows]

    
    @staticmethod
    def getByUserKeyWord(keyWord, userId):     
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.pid = Products.id and userId = :userId and name ILIKE '%' || :keyWord || '%' 
ORDER BY time_ordered DESC
''',
                              keyWord=keyWord, userId = userId) 
        return [Purchase(*row) for row in rows]

        getBySellerKeyWordBuyerId

    @staticmethod
    def getByUserKeyWordSellerId(keyWord, userId, sellerId):     
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.pid = Products.id and Purchases.userId = :userId and sellerId = :sellerId and name ILIKE '%' || :keyWord || '%' 
ORDER BY time_ordered DESC
''',
                              keyWord=keyWord, userId = userId, sellerId=sellerId) 
        return [Purchase(*row) for row in rows]

    @staticmethod
    def getByUserKeyWordDate(keyWord, userId, year, month, day):     
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.pid = Products.id and extract(year from time_ordered) = :year and extract(month from time_ordered) = :month and extract(day from time_ordered) = :day and userId = :userId and name ILIKE '%' || :keyWord || '%' 
ORDER BY time_ordered DESC
''',
                              keyWord=keyWord, userId=userId,year=year, month=month, day=day) 
        return [Purchase(*row) for row in rows]


    @staticmethod
    def getByUserKeyWordSellerIdDate(keyWord, userId, sellerId, year, month, day):     
        rows = app.db.execute('''
SELECT purchases.id, purchases.userId, Purchases.pid, Purchases.quantity, Purchases.unit_price, Purchases.time_ordered, Purchases.fulfilled, Purchases.time_fulfilled, Purchases.discountAmount
FROM Purchases, Products
WHERE Purchases.pid = Products.id and userId = :userId and extract(year from time_ordered) = :year and extract(month from time_ordered) = :month and extract(day from time_ordered) = :day and sellerId = :sellerId and name ILIKE '%' || :keyWord || '%' 
ORDER BY time_ordered DESC
''',
                              keyWord=keyWord, userId=userId, sellerId = sellerId, year=year, month=month, day=day) 
        return [Purchase(*row) for row in rows]
    

    @staticmethod
    def checkProductExists(userId, productId):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE userId = :userId and pid = :productId
''', userId = userId, productId = productId)
        if rows: 
            return True
        else:
            return False
    
    @staticmethod
    def checkSellerExists(userId, sellerId):
        rows = app.db.execute('''
SELECT Products.id
FROM Purchases, Products 
WHERE pid = Products.id and userId = :userId and sellerId= :sellerId
''', userId = userId,  sellerId=sellerId)
        if rows: 
            return True
        else:
            return False

    @staticmethod
    def purchasedFrom(userId):
        rows = app.db.execute('''
SELECT sellerId
FROM Purchases, Products 
WHERE pid = Products.id and userId = :userId 
''', userId = userId)
        ret = []
        if rows: 
            for row in rows:
                ret.append(row[0])
            return ret 
        else:
            return None

    @staticmethod
    def getAnalyticsQuantity(userId):
        rows = app.db.execute('''
SELECT pid
FROM (SELECT pid, SUM(Purchases.quantity) totalQuantity
      FROM purchases, products
      WHERE Purchases.pid = Products.id and sellerId = :userId
      GROUP BY pid) temp
ORDER BY totalQuantity DESC
LIMIT 1
''', userId = userId) 
        if rows:
            return rows[0][0]

    @staticmethod
    def getAnalyticsRevenue(userId):
        rows = app.db.execute('''
SELECT temp.pid
FROM (SELECT pid, SUM(Purchases.quantity) totalQuantity
      FROM purchases, products
      WHERE Purchases.pid = Products.id and sellerId = :userId
      GROUP BY pid) temp, Purchases
WHERE temp.pid = Purchases.pid
ORDER BY (totalQuantity*Purchases.unit_price) DESC
LIMIT 1
''', userId = userId) 
        if rows:
            return rows[0][0]

    @staticmethod
    def getAnalyticsCustomers(userId):
        rows = app.db.execute('''
SELECT COUNT(DISTINCT(userid))
FROM Purchases, Products
WHERE Purchases.pid = Products.id and sellerId = :userId
''', userId = userId) 
        if rows:
            return rows[0][0]



