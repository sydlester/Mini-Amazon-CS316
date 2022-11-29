from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime


from flask import Blueprint
bp = Blueprint('error', __name__)

@bp.route('/error')
def error():
    return render_template('error.html')

