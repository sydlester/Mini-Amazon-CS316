from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.user import User
from .models.product import Product

from flask import Blueprint
bp = Blueprint('manageInventory', __name__)

@bp.route('/manageInventory', methods=["GET", "POST"])
def manageInventory():
    products = Product.getBySeller(current_user.id) 

    productDict = {} 
    for product in products: 
        productDict[product.id] = 'static/photos/'+product.theImage

    return render_template('manageInventory.html', products = products, productDict=productDict)

