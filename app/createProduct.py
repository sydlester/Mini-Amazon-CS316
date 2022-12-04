from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
from imaplib import Int2AP
from flask_wtf.file import FileField, FileAllowed
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from .models.user import User
from .models.sellerReview import SellerReview
from .config import Config

from flask import Blueprint
bp = Blueprint('createProduct', __name__)

from flask import current_app 
from .models.product import Product


class NewProductForm(FlaskForm):
    name = StringField(label = 'Name')
    description = TextAreaField(label = 'Description')
    category = SelectField(label = 'Category', choices=[('Food', 'Food'), ('Clothes', 'Clothes'), ('Sports', 'Sports'), ('Appliances', 'Appliances'), ('Random', 'Random')])
    price = FloatField(label = 'Price')
    quantity = IntegerField(label = 'Quantity')
    available = BooleanField(label = 'Immediately Available')
    image = FileField(label = "Upload Photo")
    submit = SubmitField(label = "Create Product")

def save_image(image_file):
    image_name = image_file.filename
    image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_name)
    image_file.save(image_path)
    return image_name


@bp.route('/createProduct', methods=["GET", "POST"])
def createProduct():
    form = NewProductForm()
    if form.validate_on_submit():
            if form.image.data: 
                image_name = save_image(form.image.data)
                errorMessage = Product.createProduct(
                         form.name.data,
                         form.description.data,
                         form.category.data,
                         form.price.data,
                         form.quantity.data,
                         form.available.data,
                         current_user.id,
                         image_name
                         )
                return redirect(url_for('manageInventory.manageInventory'))

    else:
        return render_template('createProduct.html', form=form)



