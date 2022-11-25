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
SELECT ROUND(avg(rating), 1) 
FROM SellerReviews
WHERE sellerId = :sellerId
''', sellerId = sellerId)
        return rows[0][0]

    @staticmethod
    def getNumberRatings(sellerId):
        rows = app.db.execute('''
SELECT COUNT(rating)
FROM SellerReviews
WHERE sellerId = :sellerId
''', sellerId = sellerId)
        return rows[0][0]
