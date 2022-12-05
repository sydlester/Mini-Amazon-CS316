from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime
from .models.product import Product
from .models.purchase import Purchase
from .models.fulfilledPurchase import FulfilledPurchase

from flask import Blueprint
bp = Blueprint('pastPurchases', __name__)


@bp.route('/pastPurchases', methods=["GET", "POST"])
def pastPurchases():
    if current_user.is_authenticated:
        orders = Purchase.getByUser(current_user.id, False)
        purchases = Purchase.getByUser(current_user.id, True)

        orderSummaries = []
        purchaseSummaries = []
        usedOrders = []
        usedPurchases = []

        for order in orders: 
            id = order.id
            usedOrders.append(id)
            totalItems = Purchase.getTotalQuantity(id)
            totalCost = Purchase.getTotalCost(id)
            timeOrdered = order.time_ordered
            fulfillmentStatus = FulfilledPurchase.isIn(id)
            fulfillTime = order.time_fulfilled
            orderSummaries.append([id, totalItems, totalCost, timeOrdered, fulfillmentStatus, fulfillTime])
        for purchase in purchases: 
            id = purchase.id
            usedPurchases.append(id)
            totalItems = Purchase.getTotalQuantity(id)
            totalCost = Purchase.getTotalCost(id)
            timeOrdered = purchase.time_ordered
            fulfillmentStatus = FulfilledPurchase.isIn(id)
            fulfillTime = purchase.time_fulfilled
            purchaseSummaries.append([id, totalItems, totalCost, timeOrdered, fulfillmentStatus, fulfillTime])

        return render_template('pastPurchases.html', purchaseSummaries=purchaseSummaries, orderSummaries = orderSummaries)
    else:
        return render_template('pastPurchases.html', purchases=None, orders = None)
    
@bp.route('/DetailedOrder<int:id>', methods=["GET", "POST"])
def detailedOrder(id):
    lines = Purchase.getByOrder(id)
    return render_template('detailedOrder.html', lines = lines)
    

    
