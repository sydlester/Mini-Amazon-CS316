from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.product import Product
from .models.purchase import Purchase


from flask import Blueprint
bp = Blueprint('productOutput', __name__)


@bp.route('/productOutput', methods=["GET", "POST"])
def productOutput():
    k = request.form["k"] 
    products = Product.getKExpensive(k)
    return render_template('productOutput.html', k=k, products = products)
