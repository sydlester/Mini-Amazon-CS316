from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('pastPurchases', __name__)


@bp.route('/pastPurchases', methods=["GET", "POST"])
def pastPurchases():
    if current_user.is_authenticated:
        purchases = Purchase.get(current_user.id)
    else:
        purchases = None
    return render_template('pastPurchases.html', purchases=purchases)
