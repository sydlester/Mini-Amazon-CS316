from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB
import os

login = LoginManager()
login.login_view = 'users.login'

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/photos')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    from .purchasesOutput import bp as purchasesOutput_bp
    app.register_blueprint(purchasesOutput_bp)

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

    from .submitProductReview import bp as submitProductReview_bp
    app.register_blueprint(submitProductReview_bp)

    from .newProductReview import bp as newProductReview_bp
    app.register_blueprint(newProductReview_bp)

    from .submitSellerReview import bp as submitSellerReview_bp
    app.register_blueprint(submitSellerReview_bp)
    
    from .newSellerReview import bp as newSellerReview_bp
    app.register_blueprint(newSellerReview_bp)

    from .pastPurchases import bp as pastPurchases_bp
    app.register_blueprint(pastPurchases_bp)

    from .manageInventory import bp as manageInventory_bp
    app.register_blueprint(manageInventory_bp)

    from .receivedReviews import bp as receivedReviews_bp
    app.register_blueprint(receivedReviews_bp)

    from .writtenReviews import bp as writtenReviews_bp
    app.register_blueprint(writtenReviews_bp)

    from .error import bp as error_bp
    app.register_blueprint(error_bp)

    from .createProduct import bp as createProduct_bp
    app.register_blueprint(createProduct_bp)
    
    from .messageChain import bp as messageChain_bp
    app.register_blueprint(messageChain_bp)

    from .viewOrders import bp as viewOrders_bp
    app.register_blueprint(viewOrders_bp)

    from .sellerDetailedOrder import bp as sellerDetailedOrder_bp
    app.register_blueprint(sellerDetailedOrder_bp)
    
    return app


