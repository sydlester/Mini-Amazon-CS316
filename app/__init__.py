from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .reviews import bp as reviews_bp
    app.register_blueprint(reviews_bp)

    from .reviewOutput import bp as reviewOutput_bp
    app.register_blueprint(reviewOutput_bp)

    from .carts import bp as carts_bp
    app.register_blueprint(carts_bp)

    from .cartsOutput import bp as cartsOutput_bp
    app.register_blueprint(cartsOutput_bp)

    return app
