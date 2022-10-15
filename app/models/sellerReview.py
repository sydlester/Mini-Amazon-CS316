from flask import current_app as app

class SellerReview:

    def __init__(self, userId, sellerId, rating, theDescription, theDate):
        self.userId = userId
        self.sellerId = sellerId
        self.rating = rating
        self.theDescription = theDescription
        self.theDate = theDate

    @staticmethod
    def getFiveRecent(userId):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
WHERE userId = :userId
ORDER BY theDate DESC
Limit 5
''',
                              userId=userId)
        return [SellerReview(*row) for row in rows]



    