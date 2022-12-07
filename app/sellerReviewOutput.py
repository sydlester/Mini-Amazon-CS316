from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('sellerReviewOutput', __name__)


@bp.route('/sellerReviewOutput/<int:sellerId>/<int:orderBy>', methods=["GET", "POST"])
def sellerReviewOutput(sellerId, orderBy):
    if orderBy == None:
        orderBy = 5
    orderBy = int(orderBy)
    seller_reviews = SellerReview.get_by_sellerId(sellerId, orderBy)
    avgRating = SellerReview.getAverageRating(sellerId)
    num = SellerReview.getNumberRatings(sellerId)
    return render_template('sellerReviewOutput.html', sellerId = sellerId, orderBy = orderBy, seller_reviews = seller_reviews, avgRating=avgRating, num=num)
    
    
    
    
    
    
