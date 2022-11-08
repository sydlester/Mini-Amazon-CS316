from flask import render_template
from flask_login import current_user
import datetime

from .models.user import User

from flask import Blueprint
bp = Blueprint('sellers', __name__)

@bp.route('/sellers')
def inventories():
    sellers = User.get_sellers()
    return render_template('sellers.html',
                           sellers=sellers)
