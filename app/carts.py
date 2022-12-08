from flask import render_template
from flask_login import current_user
from datetime import datetime
from flask import Flask, flash, request, redirect, url_for

from .models.product import Product
from .models.cart import Cart
from .models.user import User
from .models.purchase import Purchase
from .models.saved import Saved
from .models.fulfilledPurchase import FulfilledPurchase
import decimal 
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
    return render_template('carts.html', userId=userId, user_cart = user_cart, totalCost=Cart.getTotalCost(current_user.id))

@bp.route('/cartAddToCart/<int:productId>', methods=["GET", "POST"])
def cartAddToCart(productId):
    userId = current_user.id
    quantity = 1
    if Cart.check(userId, productId): 
        Cart.add_quantity(userId, productId)
    else: 
        Cart.add_to_cart(userId, productId, quantity)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, productId = productId, user_cart=user_cart, totalCost=Cart.getTotalCost(current_user.id))

@bp.route('/cartAddFromSaved/<int:productId>', methods=["GET", "POST"])
def cartAddFromSaved(productId):
    userId = current_user.id
    quantity = 1
    if Cart.check(userId, productId): 
        Cart.add_quantity(userId, productId)
        Saved.remove_from_saved(userId, productId)
    else: 
        Cart.add_to_cart(userId, productId, quantity)
        Saved.remove_from_saved(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId, totalCost=Cart.getTotalCost(current_user.id))

@bp.route('/cartIncreaseQuantity/<int:productId>', methods=["GET", "POST"])
def cartIncreaseQuantity(productId):
    userId = current_user.id
    user_cart = Cart.add_quantity(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId, totalCost=Cart.getTotalCost(current_user.id))

@bp.route('/cartDecreaseQuantity/<int:productId>', methods=["GET", "POST"])
def cartDecreaseQuantity(productId):
    userId = current_user.id
    user_cart = Cart.remove_quantity(userId, productId)
    if Cart.getQuantity(userId, productId) <= 0:
        Cart.remove_from_cart(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId, totalCost=Cart.getTotalCost(current_user.id))

@bp.route('/cartRemoveProduct/<int:productId>', methods=["GET", "POST"])
def cartRemoveProduct(productId):
    userId = current_user.id
    user_cart = Cart.remove_from_cart(userId, productId)
    user_cart = Cart.get(userId)
    return render_template('carts.html', userId=userId, user_cart=user_cart, productId = productId, totalCost=Cart.getTotalCost(current_user.id))

@bp.route('/submitOrder', methods=["GET", "POST"])
def submitOrder():

    couponCode = request.form.get("couponCode")
    if Cart.getCouponValue(couponCode) != None:
        percentOff = Cart.getCouponValue(couponCode)
    else:
        percentOff = 0
    
    userId = current_user.id
    user_cart = Cart.get(userId)
    initialCost = Cart.getTotalCost(userId)
    actualCost = initialCost*(1-decimal.Decimal(percentOff))
    for cart_item in user_cart: 
        tempProduct = Product.get(cart_item.pid)
        if tempProduct.quantity < cart_item.quantity:
            flash('Insufficient Inventory Remaining')
            return redirect(url_for('carts.carts')) 
        if current_user.balance < actualCost:
            flash('Insufficient Balance Remaining') 
            return redirect(url_for('carts.carts')) 

    error = None
    id = Purchase.getMax()+1
    timeOrdered = datetime.now()
    for cart_item in user_cart: 
        theProduct = Product.get(cart_item.pid)
        theSeller = theProduct.sellerId
        Product.decrease_quantity(theProduct.id, cart_item.quantity)
        error = Purchase.createPurchase(id, userId, theProduct.id, cart_item.quantity, theProduct.price, timeOrdered, False, None, actualCost)
        User.increase_balance(theSeller, cart_item.quantity*cart_item.unitPrice)
    
    User.decrease_balance(userId, actualCost)
    Cart.clearUserCart(userId) 

    if current_user.is_authenticated:
        all = Purchase.getByUser(current_user.id)

        orderSummaries = []
        purchaseSummaries = []
        used = []

        for order in all: 
            id = order.id
            if order.id not in used:
                used.append(id)
                totalItems = Purchase.getTotalQuantity(id)
                totalCost = Purchase.getTotalCost(id)
                timeOrdered = order.time_ordered
                fulfillmentStatus = FulfilledPurchase.isIn(id)
                fulfillTime = order.time_fulfilled
                actualCost = order.discountAmount
                if fulfillmentStatus == False:
                    orderSummaries.append([id, totalItems, totalCost, actualCost, timeOrdered, fulfillmentStatus, fulfillTime])
                else:
                    purchaseSummaries.append([id, totalItems, totalCost, actualCost, timeOrdered, fulfillmentStatus, fulfillTime])

        return render_template('pastPurchases.html', purchaseSummaries=purchaseSummaries, orderSummaries = orderSummaries)
    else:
        return render_template('pastPurchases.html', purchases=None, orders = None)

