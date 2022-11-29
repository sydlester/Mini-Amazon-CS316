from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.productReview import ProductReview
from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('receivedReviews', __name__)

@bp.route('/receivedReviews', methods=["GET", "POST"])
def receivedReviews():
    sellerId = current_user.id
    reviews = SellerReview.get_by_sellerId(sellerId, 5)
    avg = SellerReview.getAverageRating(sellerId)
    num = SellerReview.getNumberRatings(sellerId)
    numOnes = SellerReview.getOnes(sellerId)
    numTwos = SellerReview.getTwos(sellerId)
    numThrees = SellerReview.getThrees(sellerId)
    numFours = SellerReview.getFours(sellerId)
    numFives = SellerReview.getFives(sellerId)

    
    return render_template('receivedReviews.html', reviews = reviews, num = len(reviews), sellerId = sellerId, reviewType = "received", avgRating = avg, numRating= num, numOnes = numOnes, numTwos = numTwos, numThrees = numThrees, numFours = numFours, numFives= numFives)
