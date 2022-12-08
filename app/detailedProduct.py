from flask import render_template
from flask_login import current_user
import datetime
from flask import Flask, flash, request, redirect, url_for

from .models.product import Product
from .models.productReview import ProductReview

from flask import Blueprint
bp = Blueprint('detailedProduct', __name__)

@bp.route('/detailedProduct/<int:productId>')

def detailedProduct(productId):
    if ProductReview.getRatingAverage(productId):
        avg = ProductReview.getRatingAverage(productId)
    else:
        avg = 0
    if ProductReview.getNumberRatings(productId):
        num = ProductReview.getNumberRatings(productId)
    else:
        num = 0
    if ProductReview.getOnes(productId):
        numOnes = ProductReview.getOnes(productId)
    else:
        numOnes = 0
    if ProductReview.getTwos(productId):
        numTwos = ProductReview.getTwos(productId)
    else: 
        numTwos = 0
    if ProductReview.getThrees(productId):
        numThrees = ProductReview.getThrees(productId)
    else:
        numThrees = 0

    if ProductReview.getFours(productId):
        numFours = ProductReview.getFours(productId)
    else:
        numFours = 0

    if ProductReview.getFives(productId):
        numFives = ProductReview.getFives(productId)
    else:
        numFives = 0

    name = Product.getName(productId).name
    sellers = Product.getByName(name) 

    product = Product.get(productId)
    
    if current_user.is_authenticated and Product.purchased(current_user.id) and productId in Product.purchased(current_user.id):
        wasPurchased = True
    else:
        wasPurchased = False

    if product != None:
        picture = url_for('static', filename = 'photos/'+product.theImage)
        
        return render_template('detailedProduct.html', productId = productId, product = product, avgRating = avg, numRating = num, numOnes = numOnes, 
        numTwos = numTwos, numThrees= numThrees, numFours = numFours, numFives = numFives, sellers = sellers, picture=picture, wasPurchased=wasPurchased)


       
