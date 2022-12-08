from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.productReview import ProductReview
from .models.purchase import Purchase
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

from flask import current_app 
from .models.product import Product
from .models.sellerReview import SellerReview

from flask import Blueprint
bp = Blueprint('submitSellerReview', __name__)

class NewSellerReviewForm(FlaskForm):
    description = TextAreaField(label = 'Description')
    rating = SelectField(label = 'Rating', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    image = FileField(label = "Upload Photo")
    submit = SubmitField(label = "Submit Review")
class EditSellerReviewForm(FlaskForm):
    description = TextAreaField(label = 'Description')
    rating = SelectField(label = 'Rating', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    image = FileField(label = "Upload Photo")
    submit = SubmitField(label = "Submit Review")
def save_image(image_file):
    image_name = image_file.filename
    image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_name)
    image_file.save(image_path)
    return image_name

@bp.route('/submitSellerReview/<int:sellerId>/<int:userId>', methods=["GET", "POST"])
def submitSellerReview(sellerId, userId):
    if Purchase.checkSellerExists(userId, sellerId) == False:
        return render_template("error.html", errorMessage = "You haven't purchased from this seller")
    if SellerReview.checkExists(userId, sellerId) == True: 
        return redirect (url_for('submitSellerReview.editSellerReview', sellerId = sellerId, userId = userId))
    
    form = NewSellerReviewForm()
    if form.validate_on_submit():
        if form.image.data: 
            image_name = save_image(form.image.data)
            errorMessage = SellerReview.submitSellerReview(userId, sellerId, form.rating.data, form.description.data, datetime.now(), image_name) 
            return redirect(url_for('sellerReviewOutput.sellerReviewOutput', sellerId=sellerId, orderBy=5))
    else: 
        return render_template('submitSellerReview.html', sellerId=sellerId, userId=userId, form=form) 


@bp.route('/editSellerReview/<int:sellerId>/<int:userId>', methods=["GET", "POST"])
def editSellerReview(sellerId, userId):
    form = EditSellerReviewForm()
    
    if request.method == "GET":
        review = SellerReview.getSpecific(userId, sellerId)[0]
        form.description.data = review.theDescription
        form.image.data = review.theImage
        form.rating.data = review.rating

    if form.validate_on_submit():
        if form.image.data: 
            image_name = save_image(form.image.data)
            errorMessage = SellerReview.editSellerReview(userId, sellerId, form.rating.data, form.description.data, datetime.now(), image_name) 
            return redirect(url_for('sellerReviewOutput.sellerReviewOutput', sellerId=sellerId, orderBy=5))
    else: 
        return render_template('editProductReview.html', sellerId=sellerId, userId=userId, form=form) 




