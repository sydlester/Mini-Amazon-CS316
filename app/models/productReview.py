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