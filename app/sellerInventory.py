from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.user import User
from .models.product import Product

from flask import Blueprint
bp = Blueprint('sellerInventory', __name__)

@bp.route('/sellerInventory/<int:sellerId>/<int:orderBy>', methods=["GET", "POST"])
def sellerInventory(sellerId, orderBy):
    if orderBy == None:
        orderBy = 
    orderBy = int(orderBy)
    seller_inventory = Product.getInventoryBySeller(sellerId, orderBy)
    return render_template('sellerInventory.html', sellerId = sellerId, orderBy = orderBy, seller_inventory = seller_inventory)