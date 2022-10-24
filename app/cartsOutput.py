from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.product import Product
from .models.purchase import Purchase

from .models.cart import Cart


from flask import Blueprint
bp = Blueprint('cartsOutput', __name__)


@bp.route('/cartsOutput', methods=["GET", "POST"])
def cartsOutput():
    userId = request.form["uid"] 
    user_cart = Cart.get(userId)
    
    return render_template('cartsOutput.html', userId=userId, user_cart = user_cart)
