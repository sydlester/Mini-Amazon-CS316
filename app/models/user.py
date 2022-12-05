from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

 
class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, balance, isSeller):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = balance
        self.isSeller = isSeller 
        self.user_details = {
            'User ID': ['id', self.id],
            'First Name': ['name_first', self.firstname],
            'Last Name': ['name_last', self.lastname],
            'Email': ['email', self.email]
        }

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance, isSeller
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address, isSeller):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address, balance, isSeller)
VALUES(:email, :password, :firstname, :lastname, :address, :balance, :isSeller)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, address= address, balance = 0, isSeller=isSeller)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, balance, isSeller
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def get_sellers():
        rows = app.db.execute('''
SELECT id, email, firstname, lastname, address, balance, isSeller
FROM Users
WHERE isSeller = True
''',
                              )
        return [User(*row) for row in rows]

    @staticmethod
    def isSeller(id):
        rows = app.db.execute('''
SELECT isSeller
FROM Users
WHERE id = :id
''',
                              )
        return [User(*row) for row in rows]

    @staticmethod
    def withdraw(amount):
        if amount == '':
            return False
        
        curr_balance = app.db.execute("""
SELECT balance FROM Users WHERE id = :uid
""",
                        uid = id)
        curr_bal = curr_balance[0][0]
        new_bal = curr_bal - float(amount)
        if new_bal < 0:
            return None
        else:
            self.balance = new_bal
            rows = app.db.execute("""
UPDATE Users
SET balance = :new_bal
WHERE id = :uid
RETURNING id
""",
                            new_bal = new_bal,
                            uid = id)
            return True
        
    @staticmethod
    def deposit(amount):
        if amount == '':
            return False
        curr_balance = app.db.execute("""
SELECT balance FROM Users WHERE id = :uid
""",
                        uid = id)
        curr_bal = curr_balance[0][0]
        new_bal = curr_bal + float(amount)
        self.balance = new_bal
        rows = app.db.execute("""
UPDATE Users
SET balance = :new_bal
WHERE id = :uid
RETURNING id
""",
                            new_bal = new_bal,
                            uid = id)
        return True

    @staticmethod
    def update_information(self, email, firstname, lastname):
        uid = self.id
        if email is not None:
            if self.email_exists(email):
                return False
            self.email = email
            app.db.execute("""
UPDATE Users 
SET email = :email
WHERE id = :id
RETURNING id;
""",
                            email = email,
                            id = uid)
        if firstname is not None:
            self.firstname = firstname
            app.db.execute("""
UPDATE Users 
SET firstname = :firstname
WHERE id = :id
RETURNING id;
""",
                            firstname = firstname,
                            id = uid)
            
        if lastname is not None:
            self.lastname = lastname
            app.db.execute("""
UPDATE Users 
SET lastname = :lastname
WHERE id = :id
RETURNING id;
""",
                            lastname = lastname,
                            id = uid)
        return True
