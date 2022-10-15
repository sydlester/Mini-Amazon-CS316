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
