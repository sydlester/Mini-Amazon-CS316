from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime
import math 

from .models.product import Product
from .models.purchase import Purchase

from .models.productReview import ProductReview

from flask import Blueprint
bp = Blueprint('productReviewOutput', __name__)


@bp.route('/productReviewOutput/<int:productId>/<int:orderBy>', methods=["GET", "POST"])
def productReviewOutput(productId, orderBy):
    if orderBy == None:
        orderBy = 5
    else:
        orderBy = int(orderBy)
    
    activePage = request.args.get('activePage')
    if activePage == None:
        activePage = 1
    else:
        activePage = int(activePage)
    if activePage == 1: 
        offset = 0
    else:
        offset = (activePage-1)*10

    allProductReviews = ProductReview.get_by_productId(productId, orderBy)
    total = len(allProductReviews)
    product_reviews = ProductReview.getOff(productId, offset, orderBy)
    pages = math.ceil(total/10)

    return render_template('productReviewOutput.html', product_reviews=product_reviews, activePage = activePage, pages = pages, productId=productId, orderBy=orderBy)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    if orderBy == None:
        orderBy = 5
    orderBy = int(orderBy)


    product_reviews = ProductReview.get_by_productId(productId, orderBy)

    return render_template('productReviewOutput.html', productId = productId, orderBy = orderBy, product_reviews = product_reviews)
