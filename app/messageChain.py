from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime
from .models.product import Product
from .models.purchase import Purchase
from .models.message import Message
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField
from flask import Flask, flash, request, redirect, url_for

from flask import current_app 
from .models.message import Message

from flask import Blueprint
bp = Blueprint('messageChain', __name__)

class MessageChainForm(FlaskForm):
    content = TextAreaField(label = 'New Message')
    submit = SubmitField(label = "Send")

@bp.route('/messageChain/<int:recipient>', methods=["GET", "POST"])
def messageChain(recipient):
    sender = current_user.id
    recipient = recipient
    theTime = datetime.now()

    form = MessageChainForm()
    if form.validate_on_submit():
        content = form.content.data
        errorMessage = Message.submitMessage(sender, recipient, content, theTime)
        messages = Message.getMessages(sender, recipient)
        num = len(messages)
        return redirect(url_for('messageChain.messageChain', recipient = recipient))

    else:
        messages = Message.getMessages(sender, recipient)
        num = len(messages)
        return render_template('messageChain.html', recipient=recipient, form=form, messages = messages, num = num)
