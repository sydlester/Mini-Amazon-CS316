from flask import current_app as app

class ProductReview:

    def __init__(self, userId, pid, rating, theDescription, theDate):
        self.userId = userId
        self.pid = pid
        self.rating = rating
        self.theDescription = theDescription
        self.theDate = theDate

    @staticmethod
    def getByUser(userId):
        rows = app.db.execute('''
SELECT *
FROM ProductReviews
Where userId = :userId
''', userId = userId)
        return [ProductReview(*row) for row in rows]


    @staticmethod
    def getFiveRecent(userId):
        rows = app.db.execute('''
SELECT *
FROM ProductReviews
WHERE userId = :userId
ORDER BY theDate DESC 
LIMIT 5
''',
                              userId=userId)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all(userId):
        rows = app.db.execute('''
SELECT *
FROM ProductReviews
''',)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_by_productId(productId, orderMe):
        rows = app.db.execute('''
SELECT *
FROM ProductReviews
WHERE pid = :productId
ORDER BY :orderMe DESC
''',            productId = productId, orderMe = orderMe)
        return [ProductReview(*row) for row in rows]


    @staticmethod
    def submitProductReview(userId, pid, rating, theDescription, theDate):
        rows = app.db.execute('''
INSERT INTO ProductReviews VALUES (:userId, :pid, :rating, :theDescription, :theDate)
''',
                              userId = userId, pid = pid, rating = rating, theDescription = theDescription, theDate=theDate)
        return


    @staticmethod
    def getRatingAverage(productId):
        rows = app.db.execute('''
SELECT ROUND(AVG(CAST(rating AS numeric)), 1)
FROM ProductReviews
WHERE pid = :productId
''', productId = productId)
        if rows: 
            return rows[0][0]
        else: 
            return None


    @staticmethod
    def getNumberRatings(productId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM ProductReviews
WHERE pid = :productId
''', productId = productId)
        return rows[0][0]

    @staticmethod
    def getZeros(productId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM ProductReviews
WHERE pid = :productId and rating = 0
''', productId = productId)
        return rows[0][0]

    @staticmethod
    def getOnes(productId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM ProductReviews
WHERE pid = :productId and rating = 1
''', productId = productId)
        return rows[0][0]

    @staticmethod
    def getTwos(productId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM ProductReviews
WHERE pid = :productId and rating = 2
''', productId = productId)
        return rows[0][0]

    @staticmethod
    def getThrees(productId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM ProductReviews
WHERE pid = :productId and rating = 3
''', productId = productId)
        return rows[0][0]

    @staticmethod
    def getFours(productId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM ProductReviews
WHERE pid = :productId and rating = 4
''', productId = productId)
        return rows[0][0]

    @staticmethod
    def getFives(productId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM ProductReviews
WHERE pid = :productId and rating = 5
''', productId = productId)
        return rows[0][0]

    @staticmethod
    def checkExists(userId, productId):
        rows = app.db.execute('''
SELECT *
FROM ProductReviews
WHERE userId = :userId and pid = :productId
''', userId = userId, productId = productId)
        if rows: 
            return True
        else:
            return False

    @staticmethod
    def editProductReview(userId, pid, rating, theDescription, theDate):
        rows = app.db.execute('''
UPDATE ProductReviews 
SET rating= :rating, theDescription = :theDescription, theDate = :theDate
WHERE userId = :userId and pid = :pid
''', userId=userId, pid=pid, rating=rating, theDescription=theDescription, theDate=theDate)


    @staticmethod
    def getAllByUser(userId):
        try: 
            rows = app.db.execute('''
SELECT *
FROM (
    Select pid as receiverId, rating, theDescription, theDate, 0 as type From ProductReviews WHERE userId = :userId
    UNION ALL 
    Select sellerId as receiverId, rating, theDescription, theDate, 1 as type From SellerReviews WHERE userId = :userId
) as T
ORDER BY theDate DESC
''', userId = userId)
        #ret = []
        #if rows: 
        #    for row in rows: 
        #        ret.append(row)
            return rows
        except Exception as e:
            return str(e)

    @staticmethod
    def getOff(productId, os, orderMe):
        rows = app.db.execute('''
SELECT *
FROM ProductReviews
WHERE pid = :productId
ORDER BY :orderMe DESC
LIMIT 10
OFFSET :os
''',
                              productId=productId, os = os, orderMe=orderMe)
        return [ProductReview(*row) for row in rows]