from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.productReview import ProductReview
from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('writtenReviews', __name__)


@bp.route('/writtenReviews', methods=["GET", "POST"])
def writtenReviews():
    reviews = ProductReview.getAllByUser(current_user.id)
    return render_template('writtenReviews.html', reviewType = "written", reviews = reviews)
