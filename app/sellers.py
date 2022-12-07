from flask import render_template
from flask_login import current_user
import datetime
from flask import request 
from .models.user import User
from .models.purchase import Purchase
import math
from flask import Blueprint
bp = Blueprint('sellers', __name__)

@bp.route('/sellers')
def sellers():
    
    activePage = request.args.get('activePage')
    if activePage == None:
        activePage = 1
    else:
        activePage = int(activePage)
    if activePage == 1: 
        offset = 0
    else:
        offset = (activePage-1)*10
    all = User.getAll()
    total = len(all)
    pages = math.ceil(total/10)
    usersSellers = User.getOff(offset)

    purchasedFrom = Purchase.purchasedFrom(current_user.id)
    return render_template('sellers.html',
                           usersSellers=usersSellers, purchasedFrom = purchasedFrom, activePage=activePage, pages=pages)
