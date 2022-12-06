from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.sellerReview import SellerReview
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('submitSellerReview', __name__)

@bp.route('/submitSellerReview/<int:sellerId>/<int:userId>', methods=["GET", "POST"])
def submitSellerReview(sellerId, userId):
    if Purchase.checkSellerExists(userId, sellerId) == False:
        return render_template("error.html", errorMessage = "You haven't purchased from this seller")
    if SellerReview.checkExists(userId, sellerId) == True: 
        return render_template("editSellerReview.html", sellerId=sellerId, userId=userId) 
    else: 
        return render_template('submitSellerReview.html', sellerId = sellerId, userId= userId)





