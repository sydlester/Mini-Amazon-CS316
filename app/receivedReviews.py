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
    avg = SellerReview.getAverageRating(sellerId)
    num = SellerReview.getNumberRatings(sellerId)
    return render_template('receivedReviews.html', sellerId = sellerId, reviewType = "received", avgRating = avg, numRating= num)
