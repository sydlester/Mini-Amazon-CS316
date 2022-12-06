from flask import render_template
from flask_login import current_user
from flask import request
import math 
import datetime
from flask import Flask, flash, request, redirect, url_for
from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('products', __name__)

@bp.route('/products/', methods=['GET', 'POST'])
def products():
    activePage = request.args.get('activePage')
    if activePage == None:
        activePage = 1
    else:
        activePage = int(activePage)

    if activePage == 1: 
        offset = 0
    else:
        offset = (activePage-1)*5


    if request.method == "GET":
        allProducts = Product.get_all(True)
        total = len(allProducts)

        products = Product.getOff(True, offset)
        pages = math.ceil(total/5)

        productDict = {} 
        for product in allProducts: 
            productDict[product.id] = url_for('static', filename = 'photos/'+product.theImage)
        return render_template('products.html', avail_products=products, theMax = 500, theMin = 1, pages = pages, activePage = activePage, productDict = productDict)


    elif request.method == "POST":
        keyWord = request.form["searchField"]
        myMax = request.form["maxPrice"]
        minRating = request.form["minRating"]
        category = request.form["category"]

        if category == "Select":
            allProducts = Product.noCat(keyWord, myMax, minRating, None, None)
            products = Product.noCat(keyWord, myMax, minRating, 5, offset)
            
        else:
            allProducts = Product.getByKeyWord(keyWord, myMax, minRating, category, None, None)
            products = Product.getByKeyWord(keyWord, myMax, minRating, category, 5, offset)

        total = len(allProducts)
        pages = math.ceil(total/5)

        productDict = {} 
        for product in allProducts: 
            productDict[product.id] = url_for('static', filename = 'photos/'+product.theImage)


        return render_template('products.html',
                           avail_products=products, category = category, theMax = myMax, theMin = minRating, activePage = activePage, pages = pages, productDict = productDict)

