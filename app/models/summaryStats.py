from flask import current_app as app

class SummaryStats:

    def __init__(self, stat):
        self.stat = stat

    @staticmethod
    def getAvgProductRating(productId):
        rows = app.db.execute('''
SELECT avg(rating) as avgRating
FROM ProductReviews
Where pid = :productId
''', productId = productId)
        return [SummaryStats(*row) for row in rows]


    @staticmethod
    def getNumProductReviews(productId):
        rows = app.db.execute('''
SELECT count(rating) as numRatings
FROM ProductReviews
Where pid = :productId
''', productId = productId)
        return [SummaryStats(*row) for row in rows]

   
 
