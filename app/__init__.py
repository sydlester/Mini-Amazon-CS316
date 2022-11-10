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

    from .carts import bp as carts_bp
    app.register_blueprint(carts_bp)

    from .products import bp as products_bp
    app.register_blueprint(products_bp)

    from .sellers import bp as sellers_bp
    app.register_blueprint(sellers_bp)

    from .purchase import bp as purchase_bp
    app.register_blueprint(purchase_bp)

    from .productReviewOutput import bp as productReviewOutput_bp
    app.register_blueprint(productReviewOutput_bp)

    from .sellerReviewOutput import bp as sellerReviewOutput_bp
    app.register_blueprint(sellerReviewOutput_bp)

    from .account import bp as account_bp
    app.register_blueprint(account_bp)

    from .detailedProduct import bp as detailedProduct_bp
    app.register_blueprint(detailedProduct_bp)

    from .detailedSeller import bp as detailedSeller_bp
    app.register_blueprint(detailedSeller_bp)

    return app
