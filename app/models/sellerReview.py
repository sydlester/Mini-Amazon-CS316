from flask import current_app as app

class SellerReview:

    def __init__(self, userId, sellerId, rating, theDescription, theDate):
        self.userId = userId
        self.sellerId = sellerId
        self.rating = rating
        self.theDescription = theDescription
        self.theDate = theDate

    @staticmethod
    def getByUser(userId):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
Where userId = :userId
''', userId = userId)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def get_all(userId):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
''',)
        return [SellerReview(*row) for row in rows]


    @staticmethod
    def get_by_sellerId(sellerId, orderMe):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
WHERE sellerId = :sellerId
ORDER BY :orderMe DESC
''',                sellerId = sellerId, orderMe = orderMe)
        return [SellerReview(*row) for row in rows]



    @staticmethod
    def submitSellerReview(userId, sellerId, rating, theDescription, theDate):
        rows = app.db.execute('''
INSERT INTO SellerReviews VALUES (:userId, :sellerId, :rating, :theDescription, :theDate)
''',
                              userId = userId, sellerId = sellerId, rating = rating, theDescription = theDescription, theDate=theDate)
        return

    @staticmethod
    def getAverageRating(sellerId):
        rows = app.db.execute('''
SELECT ROUND(CAST(rating AS numeric),1) 
FROM SellerReviews
WHERE sellerId = :sellerId
''', sellerId = sellerId)
        if rows: 
            return rows[0][0]
        else: 
            return None

    @staticmethod
    def getNumberRatings(sellerId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM SellerReviews
WHERE sellerId = :sellerId
''', sellerId = sellerId)
        return rows[0][0]

    @staticmethod
    def getZeros(sellerId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM SellerReviews
WHERE sellerId = :sellerId and rating = 0
''', sellerId = sellerId)
        return rows[0][0]

    @staticmethod
    def getOnes(sellerId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM SellerReviews
WHERE sellerId = :sellerId and rating = 1
''', sellerId = sellerId)
        return rows[0][0]

    @staticmethod
    def getTwos(sellerId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM SellerReviews
WHERE sellerId = :sellerId and rating = 2
''', sellerId = sellerId)
        return rows[0][0]

    @staticmethod
    def getThrees(sellerId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM SellerReviews
WHERE sellerId = :sellerId and rating = 3
''', sellerId = sellerId)
        return rows[0][0]

    @staticmethod
    def getFours(sellerId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM SellerReviews
WHERE sellerId = :sellerId and rating = 4
''', sellerId = sellerId)
        return rows[0][0]

    @staticmethod
    def getFives(sellerId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM SellerReviews
WHERE sellerId = :sellerId and rating = 5
''', sellerId = sellerId)
        return rows[0][0]