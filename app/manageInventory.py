from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.user import User
from .models.product import Product

from flask import Blueprint
bp = Blueprint('manageInventory', __name__)

@bp.route('/manageInventory', methods=["GET", "POST"])
def manageInventory():
    return render_template('manageInventory.html')

