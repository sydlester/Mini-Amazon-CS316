from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('detailedProduct', __name__)


@bp.route('/detailedProduct/<int:productId>')
def detailedProduct(productId):
    return render_template('detailedProduct.html', productId = productId)

