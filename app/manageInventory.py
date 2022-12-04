from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime
from flask import Flask, flash, request, redirect, url_for

from .models.user import User
from .models.product import Product

from flask import Blueprint
bp = Blueprint('manageInventory', __name__)


@bp.route('/increaseInventoryQuantity/<int:productId>', methods=["GET", "POST"])
def increaseInventoryQuantity(productId):
    userId = current_user.id
    Product.add_quantity(userId, productId)
    products = Product.getBySeller(userId)
    productDict = {} 
    for product in products: 
        productDict[product.id] = url_for('static', filename = 'photos/'+product.theImage)
    return render_template('manageInventory.html', products= products, productDict = productDict)

@bp.route('/decreaseInventoryQuantity/<int:productId>', methods=["GET", "POST"])
def decreaseInventoryQuantity(productId):
    userId = current_user.id
    Product.decrease_quantity(userId, productId)
    products = Product.getBySeller(userId)
    productDict = {} 
    for product in products: 
        productDict[product.id] = url_for('static', filename = 'photos/'+product.theImage)
    return render_template('manageInventory.html', products= products, productDict = productDict)

@bp.route('/removeFromInventory/<int:productId>', methods=["GET", "POST"])
def removeFromInventory(productId):
    userId = current_user.id
    Product.removeFromInventory(userId, productId)
    products = Product.getBySeller(userId)
    
    productDict = {} 
    for product in products: 
        productDict[product.id] = url_for('static', filename = 'photos/'+product.theImage)
    return render_template('manageInventory.html', products= products, productDict = productDict)



@bp.route('/manageInventory', methods=["GET", "POST"])
def manageInventory():
    products = Product.getBySeller(current_user.id) 

    productDict = {} 
    for product in products: 
        productDict[product.id] = url_for('static', filename = 'photos/'+product.theImage)

    return render_template('manageInventory.html', products = products, productDict=productDict)

