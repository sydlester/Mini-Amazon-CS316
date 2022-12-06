from flask import render_template
from flask_login import current_user
import datetime

from .models.user import User
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('sellers', __name__)

@bp.route('/sellers')
def sellers():
    usersSellers = User.getAll()
    purchasedFrom = Purchase.purchasedFrom(current_user.id)
    return render_template('sellers.html',
                           usersSellers=usersSellers, purchasedFrom = purchasedFrom)
