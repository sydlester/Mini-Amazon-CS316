from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.productReview import ProductReview

from flask import Blueprint
bp = Blueprint('detailedProduct', __name__)

@bp.route('/detailedProduct/<int:productId>')

def detailedProduct(productId):
    avg = ProductReview.getRatingAverage(productId)
    num = ProductReview.getNumberRatings(productId)
    numOnes = ProductReview.getOnes(productId)
    numTwos = ProductReview.getTwos(productId)
    numThrees = ProductReview.getThrees(productId)
    numFours = ProductReview.getFours(productId)
    numFives = ProductReview.getFives(productId)

    name = Product.getName(productId).name
    sellers = Product.getByName(name) 

    product = Product.get(productId)
    if product != None:
        return render_template('detailedProduct.html', productId = productId, product = product, avgRating = avg, numRating = num, numOnes = numOnes, 
        numTwos = numTwos, numThrees= numThrees, numFours = numFours, numFives = numFives, sellers = sellers)


       
