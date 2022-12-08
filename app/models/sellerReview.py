from flask import current_app as app

class SellerReview:

    def __init__(self, userId, sellerId, rating, theDescription, theDate, theImage, upvotes):
        self.userId = userId
        self.sellerId = sellerId
        self.rating = rating
        self.theDescription = theDescription
        self.theDate = theDate
        self.theImage = theImage
        self.upvotes = upvotes

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
    def submitSellerReview(userId, sellerId, rating, theDescription, theDate, theImage):
        rows = app.db.execute('''
INSERT INTO SellerReviews VALUES (:userId, :sellerId, :rating, :theDescription, :theDate, :theImage, 0)
''',
                              userId = userId, sellerId = sellerId, rating = rating, theDescription = theDescription, theDate=theDate, theImage=theImage)
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
    
    @staticmethod
    def checkExists(userId, sellerId):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews 
WHERE userId = :userId and sellerId= :sellerId
''', userId = userId,  sellerId=sellerId)
        if rows: 
            return True
        else:
            return False
    
    @staticmethod
    def editSellerReview(userId, sellerId, rating, theDescription, theDate):
        rows = app.db.execute('''
UPDATE SellerReviews 
SET rating= :rating, theDescription = :theDescription, theDate = :theDate
WHERE userId = :userId and sellerId = :sellerId
''', userId=userId, sellerId=sellerId, rating=rating, theDescription= theDescription, theDate=theDate)


    @staticmethod
    def getOff(sellerId, os, orderMe):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
WHERE sellerId = :sellerId
ORDER BY :orderMe DESC
LIMIT 10
OFFSET :os
''',
                              sellerId=sellerId, os = os, orderMe=orderMe)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def addUpvotes(userId, sellerId):
        try:
            rows = app.db.execute("""
UPDATE SellerReviews
    SET upvotes = upvotes + 1 
    WHERE userId = :userId and sellerId = :sellerId
""", userId=userId, sellerId=sellerId)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            return str(e)

    @staticmethod
    def getTop3(sellerId, orderMe):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
WHERE sellerId = :sellerId
ORDER BY upvotes DESC, :orderMe DESC
LIMIT 3
''',
                              sellerId, orderMe=orderMe)
        return [SellerReview(*row) for row in rows]