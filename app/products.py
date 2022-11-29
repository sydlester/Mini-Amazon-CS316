from flask import render_template
from flask_login import current_user
from flask import request

import datetime

from .models.product import Product
from .models.purchase import Purchase


from flask import Blueprint
bp = Blueprint('products', __name__)

@bp.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == "GET":
        products = Product.get_all(True)
        return render_template('products.html',
                           avail_products=products, theMax = 500, theMin = 1)
    elif request.method == "POST":
        keyWord = request.form["searchField"]
        myMax = request.form["maxPrice"]
        minRating = request.form["minRating"]
        category = request.form["category"]
        if category == "Select":
            products = Product.noCat(keyWord, myMax, minRating)
        else:
            products = Product.getByKeyWord(keyWord, myMax, minRating, category)
        return render_template('products.html',
                           avail_products=products, category = category, theMax = myMax, theMin = minRating, length = len(products))

    