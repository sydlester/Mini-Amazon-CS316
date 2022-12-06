from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
from imaplib import Int2AP


from .models.user import User
from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('newSellerReview', __name__)

@bp.route('/newSellerReview/<int:sellerId>/<int:userId>', methods=["GET", "POST"])
def newSellerReview(sellerId, userId):
    rating = request.form["rating"]
    description = request.form["description"]
    theDate = datetime.now()
    SellerReview.submitSellerReview(userId, sellerId, rating, description, theDate)
    seller_reviews = SellerReview.get_by_sellerId(sellerId, 5)
    return render_template('sellerReviewOutput.html', sellerId = sellerId, orderBy = 5, seller_reviews = seller_reviews)

@bp.route('/editSellerReview/<int:sellerId>/<int:userId>', methods=["GET", "POST"])
def editSellerReview(sellerId, userId):
    rating = request.form["rating"]
    description = request.form["description"]
    theDate = datetime.now()
    SellerReview.editSellerReview(userId, sellerId, rating, description, theDate)
    seller_reviews = SellerReview.get_by_sellerId(sellerId, 5)
    return render_template('sellerReviewOutput.html', sellerId = sellerId, orderBy = 5, seller_reviews=seller_reviews)




