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

@bp.route('/increaseQuantity/<int:id>', methods=["GET", "POST"])
def increaseQuantity(id):
    sellerId = current_user.id
    seller_inventory = Product.add_quantity(sellerId, id)
    seller_inventory = Product.getInventoryBySeller(sellerId, 3)
    return render_template('sellerInventory.html', sellerId=sellerId, seller_inventory=seller_inventory, id = id)

@bp.route('/decreaseQuantity/<int:id>', methods=["GET", "POST"])
def decreaseQuantity(id):
    sellerId = current_user.id
    seller_inventory = Product.decrease_quantity(sellerId, id)
    seller_inventory = Product.getInventoryBySeller(sellerId, 3)
    return render_template('sellerInventory.html', sellerId=sellerId, seller_inventory=seller_inventory, id = id)

@bp.route('/removeProduct/<int:id>', methods=["GET", "POST"])
def removeProduct(id):
    sellerId = current_user.id
    seller_inventory = Product.removeFromInventory(sellerId, id)
    seller_inventory = Product.getInventoryBySeller(sellerId, 3)
    return render_template('sellerInventory.html', sellerId=sellerId, seller_inventory=seller_inventory, id = id)
