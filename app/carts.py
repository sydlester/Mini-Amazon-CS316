from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('carts', __name__)

@bp.route('/carts')
def carts():
    if current_user.is_authenticated:
        userId = current_user.id
        user_cart = Cart.get(userId)
    else:
        userId = None
        user_cart = None
    return render_template('carts.html', userId=userId, user_cart = user_cart)

@bp.route('/cartAddToCart/<int:productId>', methods=["GET", "POST"])
def cartAddToCart(productId):
    userId = current_user.id
    quantity = 1
    if Cart.check(userId, productId): 
        Cart.add_quantity(userId, productId)
    else: 
        Cart.add_to_cart(userId, productId, quantity)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, productId = productId, user_cart=user_cart)

@bp.route('/cartIncreaseQuantity/<int:productId>', methods=["GET", "POST"])
def cartIncreaseQuantity(productId):
    userId = current_user.id
    user_cart = Cart.add_quantity(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId)

@bp.route('/cartDecreaseQuantity/<int:productId>', methods=["GET", "POST"])
def cartDecreaseQuantity(productId):
    userId = current_user.id
    user_cart = Cart.remove_quantity(userId, productId)
    if Cart.getQuantity(userId, productId) <= 0:
        Cart.remove_from_cart(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId)

@bp.route('/cartRemoveProduct/<int:productId>', methods=["GET", "POST"])
def cartRemoveProduct(productId):
    userId = current_user.id
    user_cart = Cart.remove_from_cart(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId)