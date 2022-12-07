from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime
import math

from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('sellerReviewOutput', __name__)


@bp.route('/sellerReviewOutput/<int:sellerId>/<int:orderBy>', methods=["GET", "POST"])
def sellerReviewOutput(sellerId, orderBy):
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
    allSellerReviews = SellerReview.get_by_sellerId(sellerId, orderBy)
    total = len(allSellerReviews)

    seller_reviews = SellerReview.getOff(sellerId, offset, orderBy)
    pages = math.ceil(total/10)
    avgRating = SellerReview.getAverageRating(sellerId)
    num = SellerReview.getNumberRatings(sellerId)

    return render_template('sellerReviewOutput.html', seller_reviews=seller_reviews, activePage = activePage, pages = pages, sellerId=sellerId, orderBy=orderBy, avgRating=avgRating, num=num)


    
    
    
    


    
    
    
    
    
    
