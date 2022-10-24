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
bp = Blueprint('purchasesOutput', __name__)


@bp.route('/purchasesOutput', methods=["GET", "POST"])
def purchasesOutput():
    userId = request.form["uid"] 
    purchases = Purchase.get(userId)
    return render_template('purchasesOutput.html', userId=userId, user_purchases = purchases)