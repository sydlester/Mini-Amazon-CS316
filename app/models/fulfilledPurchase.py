from flask import current_app as app

class FulfilledPurchase:
    def __init__(self, id, purchaseId):
        self.id = id
        self.purchaseId = id

    @staticmethod
    def addPurchase(purchaseId):
        try:
            rows = app.db.execute("""
INSERT INTO FulfilledPurchases(purchaseId)
VALUES(:purchaseId) 
RETURNING id
""", purchaseId=purchaseId)
            return FulfilledPurchase.get(id)
        except Exception as e:
            return str(e)
    
    @staticmethod
    def isIn(purchaseId):
        rows = app.db.execute("""
SELECT * 
FROM FulfilledPurchases
WHERE purchaseId = :purchaseId
""", purchaseId=purchaseId)
        if rows: 
            return True
        else:
            return False

    
    