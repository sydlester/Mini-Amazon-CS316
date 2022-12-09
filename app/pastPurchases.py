from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime
from .models.product import Product
from .models.purchase import Purchase
from .models.fulfilledPurchase import FulfilledPurchase
from flask import Blueprint
from datetime import datetime

bp = Blueprint('pastPurchases', __name__)

@bp.route('/pastPurchases', methods=["GET", "POST"])
def pastPurchases():
    if current_user.is_authenticated:

        if request.method == "GET":
            all = Purchase.getByUser(current_user.id)

        elif request.method == "POST":
            searchField = request.form["searchField"]
            sellerId = request.form["sellerId"]
            date = request.form["date"]
            if date != "":
                date = datetime.strptime(request.form["date"], '%Y-%m-%d')
                month = date.month
                year = date.year
                day = date.day

            if sellerId == "" and date == "":
                all = Purchase.getByUserKeyWord(searchField, current_user.id)
            elif sellerId != "" and date == "":
                all = Purchase.getByUserKeyWordSellerId(searchField, current_user.id, sellerId)
            elif sellerId == "" and date != "": 
                all = Purchase.getByUserKeyWordDate(searchField, current_user.id, year, month, day)
            else:
                all = Purchase.getByUserKeyWordSellerIdDate(searchField, current_user.id, sellerId, year, month, day)

        orderSummaries = []
        purchaseSummaries = []
        used = []

        for order in all: 
            id = order.id
            if order.id not in used:
                used.append(id)
                totalItems = Purchase.getTotalQuantity(id)
                totalCost = Purchase.getTotalCost(id)
                timeOrdered = order.time_ordered
                fulfillmentStatus = FulfilledPurchase.isIn(id)
                fulfillTime = order.time_fulfilled
                actualCost = order.discountAmount
                if fulfillmentStatus == False:
                    orderSummaries.append([id, totalItems, totalCost, actualCost, timeOrdered, fulfillmentStatus, fulfillTime])
                else:
                    purchaseSummaries.append([id, totalItems, totalCost, actualCost, timeOrdered, fulfillmentStatus, fulfillTime])

        return render_template('pastPurchases.html', purchaseSummaries=purchaseSummaries, orderSummaries = orderSummaries)
    else:
        return render_template('pastPurchases.html', purchases=None, orders = None)


@bp.route('/DetailedOrder<int:id>', methods=["GET", "POST"])
def detailedOrder(id):
    lines = []
    lineItems = Purchase.getByOrder(id)

    for item in lineItems:
        id = item.id
        pid = item.pid 
        quantity = item.quantity
        unit_price = item.unit_price
        time_ordered = item.time_ordered
        fulfilled = item.fulfilled
        time_fulfilled = item.time_fulfilled 
        totalLineCost = quantity*unit_price 
        productName = Product.get(pid).name
        sellerId = Product.get(pid).sellerId
        lines.append([id, pid, productName, sellerId, quantity, unit_price, totalLineCost, time_ordered, fulfilled, time_fulfilled])
    
    return render_template('detailedOrder.html', lines = lines)
    

    
