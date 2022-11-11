from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('submitSellerReview', __name__)

@bp.route('/submitSellerReview/<int:sellerId>/<int:userId>', methods=["GET", "POST"])
def submitSellerReview(sellerId, userId):
    return render_template('submitSellerReview.html', sellerId = sellerId, userId= userId)


