from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.product import Product


from flask import Blueprint
bp = Blueprint('editInventory', __name__)

@bp.route('/editInventory/<int:productId>', methods=["GET", "POST"])
def editInventory(productId):
    return render_template('editInventory.html', productId = productId)
