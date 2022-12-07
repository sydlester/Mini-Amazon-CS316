from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime

from .models.user import User
from .models.productReview import ProductReview

from flask import Blueprint
bp = Blueprint('newProductReview', __name__)

@bp.route('/newProductReview/<int:productId>/<int:userId>', methods=["GET", "POST"])
def newProductReview(productId, userId):
    rating = request.form["rating"]
    description = request.form["description"]
    theDate = datetime.now()
    ProductReview.submitProductReview(userId, productId, rating, description, theDate)
    product_reviews = ProductReview.get_by_productId(productId, 5)
    return render_template('productReviewOutput.html', productId = productId, orderBy = 5, product_reviews=product_reviews)


@bp.route('/editProductReview/<int:productId>/<int:userId>', methods=["GET", "POST"])
def editProductReview(productId, userId):
    if request.method == "POST":
        rating = request.form["rating"]
        description = request.form["description"]
        theDate = datetime.now()
        ProductReview.editProductReview(userId, productId, rating, description, theDate)
        product_reviews = ProductReview.get_by_productId(productId, 5)
        return render_template('productReviewOutput.html', productId = productId, orderBy = 5, product_reviews=product_reviews)
    else:
        return render_template("editProductReview.html", productId=productId, userId=userId) 

