from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchase', __name__)


@bp.route('/purchase')
def purchase():
    return render_template('purchase.html')