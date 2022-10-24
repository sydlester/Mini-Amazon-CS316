from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.product import Product
from .models.purchase import Purchase


from flask import Blueprint
bp = Blueprint('inventoryOutput', __name__)


@bp.route('/inventoryOutput', methods=["GET", "POST"])
def inventoryOutput():
    sellerId = request.form["sellerId"] 
    inventory = Product.getBySeller(sellerId)
    return render_template('inventoryOutput.html', sellerId=sellerId, inventory = inventory)
