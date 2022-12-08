from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.product import Product

from flask import Blueprint
bp = Blueprint('editInventorySuccess', __name__)

@bp.route('/editInventorySuccess/<int:productId>', methods=["GET", "POST"])
def editInventorySuccess(productId):
    quantityNew = request.form["quantityNew"]
    sellerId = current_user.id
    Product.editInventory(sellerId, productId, quantityNew)
    return render_template('editInventorySuccess.html', productId = productId)
