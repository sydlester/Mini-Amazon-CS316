from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase


from flask import Blueprint
bp = Blueprint('inventories', __name__)

@bp.route('/inventories')
def inventories():
    return render_template('inventories.html')
