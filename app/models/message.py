from flask import current_app as app

class Message:
    def __init__(self, id, sender, recipient, content, theTime):
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.content = content 
        self.theTime = theTime

    @staticmethod
    def submitMessage(sender, recipient, content, theTime):
        try:
            rows = app.db.execute("""
INSERT INTO Messages(sender, recipient, content, theTime)
VALUES(:sender, :recipient, :content, :theTime)
RETURNING id
""", sender = sender, recipient = recipient, content = content, theTime = theTime)
            id = rows[0][0]
            return Message.get(id)
        except Exception as e:
            return str(e)


    @staticmethod
    def getMessages(sender, recipient):
        rows = app.db.execute('''
SELECT *
FROM Messages
Where (sender = :sender and recipient = :recipient) OR (sender = :recipient and recipient = :sender)
Order by 5 
''', sender = sender, recipient = recipient)
        return [Message(*row) for row in rows]
    