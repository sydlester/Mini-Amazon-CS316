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
bp = Blueprint('viewOrders', __name__)
from flask import current_app 
from .models.product import Product
from .models.purchase import Purchase
from .models.fulfilledPurchase import FulfilledPurchase

@bp.route('/viewOrders', methods=["GET", "POST"])
def viewOrders():
    if request.method == "GET":
        orders = Purchase.getAllBySeller(current_user.id)

    elif request.method == "POST":
        searchField = request.form["searchField"]
        buyerId = request.form["buyerId"]
        date = request.form["date"]
        if date != "":
            date = datetime.strptime(request.form["date"], '%Y-%m-%d')
            month = date.month
            year = date.year
            day = date.day

        if buyerId == "" and date == "":
            orders = Purchase.getBySellerKeyWord(searchField, current_user.id)
        elif buyerId != "" and date == "":
            orders = Purchase.getBySellerKeyWordBuyerId(searchField, buyerId, current_user.id)
        elif buyerId == "" and date != "": 
             orders = Purchase.getBySellerKeyWordDate(searchField, current_user.id, year, month, day)
        else:
            orders = Purchase.getBySellerKeyWordBuyerIdDate(searchField, current_user.id, buyerId, year, month, day)

    
    orderSummaries = []
    used = []
    if orders == None:
        return render_template('error.html', errorMessage = "No Orders Yet!")
    
    for order in orders: 
        id = order.id
        if id not in used:
            used.append(id)
            userId = order.userId
            userObject = User.get(userId)
            name = userObject.firstname + " " + userObject.lastname
            address = userObject.address
            email = userObject.email
            orderDate = order.time_ordered
            totalCost = Purchase.getTotalCostSeller(id, current_user.id)
            totalQuantity = Purchase.getTotalQuantitySeller(id, current_user.id)
            fulfillment = FulfilledPurchase.isIn(id)
            orderSummaries.append([id, userId, name, address, email, orderDate, totalCost, totalQuantity, fulfillment])
            analyticsQuantity = Purchase.getAnalyticsQuantity(current_user.id)
            analyticsRevenue = 1
            analyticsCustomers = Purchase.getAnalyticsCustomers(current_user.id)
    return render_template('viewOrders.html', orderSummaries=orderSummaries, analyticsQuantity = analyticsQuantity, analyticsRevenue = analyticsRevenue, analyticsCustomers = analyticsCustomers)

@bp.route('/fulfillOrder/<int:id>/<int:pid>/<int:userId>', methods=["GET", "POST"])
def fulfillOrder(id, pid, userId):
    wasFulfilled = bool(request.form["fulfilled"])
    if wasFulfilled == True: 
        error = Purchase.markFulfilled(id, pid, userId)
        if error: 
            return render_template("error.html", errorMessage=error)
        purchases = Purchase.getByOrder(id)
        for purchase in purchases: 
            if purchase.fulfilled == False:
                return redirect(url_for('sellerDetailedOrder.sellerDetailedOrder', id = id))
        FulfilledPurchase.addPurchase(id)
    return redirect(url_for('sellerDetailedOrder.sellerDetailedOrder', id = id))
    
