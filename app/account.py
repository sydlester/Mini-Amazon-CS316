from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User


from flask import Blueprint
bp = Blueprint('account', __name__)


@bp.route('/account')
def account():
    return render_template('account.html')
