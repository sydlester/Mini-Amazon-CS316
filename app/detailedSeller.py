from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('detailedSeller', __name__)


@bp.route('/detailedSeller/<int:sellerId>')
def detailedSeller(sellerId):
    seller_inventory = Product.getBySeller(sellerId)
    return render_template('detailedSeller.html', sellerId = sellerId, seller_inventory = seller_inventory)



