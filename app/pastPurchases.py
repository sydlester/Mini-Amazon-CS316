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
        all = Purchase.getByUser(current_user.id)

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
                if fulfillmentStatus == False:
                    orderSummaries.append([id, totalItems, totalCost, timeOrdered, fulfillmentStatus, fulfillTime])
                else:
                    purchaseSummaries.append([id, totalItems, totalCost, timeOrdered, fulfillmentStatus, fulfillTime])

        return render_template('pastPurchases.html', purchaseSummaries=purchaseSummaries, orderSummaries = orderSummaries)
    else:
        return render_template('pastPurchases.html', purchases=None, orders = None)
    
@bp.route('/DetailedOrder<int:id>', methods=["GET", "POST"])
def detailedOrder(id):
    lines = Purchase.getByOrder(id)
    return render_template('detailedOrder.html', lines = lines)
    

    
