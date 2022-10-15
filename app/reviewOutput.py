from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.product import Product
from .models.purchase import Purchase

from .models.productReview import ProductReview
from .models.sellerReview import SellerReview


from flask import Blueprint
bp = Blueprint('reviewOutput', __name__)


@bp.route('/reviewOutput', methods=["GET", "POST"])
def reviewOutput():
    userId = request.form["uid"] 
    product_reviews = ProductReview.getFiveRecent(userId)
    seller_reviews = SellerReview.getFiveRecent(userId)
    return render_template('reviewOutput.html', userId=userId, product_reviews = product_reviews, seller_reviews = seller_reviews)
