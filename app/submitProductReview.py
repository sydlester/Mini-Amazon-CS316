from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('submitProductReview', __name__)

@bp.route('/submitProductReview/<int:productId>/<int:userId>', methods=["GET", "POST"])
def submitProductReview(productId, userId):
    return render_template('submitProductReview.html', productId = productId, userId= userId)


