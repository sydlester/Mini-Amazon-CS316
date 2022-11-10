from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('carts', __name__)


@bp.route('/carts')
def carts():
    userId = current_user.id
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart = user_cart)

@bp.route('/addToCart/<int:productId>', methods=["GET", "POST"])
def addToCart(productId):
    userId = current_user.id
    quantity = 1
    user_cart = Cart.add_to_cart(userId, productId, quantity)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, productId = productId, user_cart=user_cart)

@bp.route('/increaseQuantity/<int:productId>', methods=["GET", "POST"])
def increaseQuantity(productId):
    userId = current_user.id
    user_cart = Cart.add_quantity(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId)

@bp.route('/decreaseQuantity/<int:productId>', methods=["GET", "POST"])
def decreaseQuantity(productId):
    userId = current_user.id
    user_cart = Cart.remove_quantity(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId)

@bp.route('/removeProduct/<int:productId>', methods=["GET", "POST"])
def removeProduct(productId):
    userId = current_user.id
    user_cart = Cart.remove_from_cart(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId)