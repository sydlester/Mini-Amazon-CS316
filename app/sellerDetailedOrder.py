from flask import render_template
from flask_login import current_user
import datetime
from .models.user import User
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('sellerDetailedOrder', __name__)

@bp.route('/sellerDetailedOrder<int:id>', methods=["GET", "POST"])
def sellerDetailedOrder(id):
    lines = Purchase.getByOrderSeller(id, current_user.id)
    return render_template('sellerDetailedOrder.html', lines = lines)