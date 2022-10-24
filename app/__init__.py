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

    from .products import bp as products_bp
    app.register_blueprint(products_bp)

    from .productOutput import bp as productOutput_bp
    app.register_blueprint(productOutput_bp)

    from .inventories import bp as inventories_bp
    app.register_blueprint(inventories_bp)

    from .inventoryOutput import bp as inventoryOutput_bp
    app.register_blueprint(inventoryOutput_bp)

    from .purchase import bp as purchase_bp
    app.register_blueprint(purchase_bp)

    from .purchasesOutput import bp as purchasesOutput_bp
    app.register_blueprint(purchasesOutput_bp)

    return app
