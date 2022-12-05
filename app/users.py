from xmlrpc.client import Boolean
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    address = StringField('Address', validators=[DataRequired()])
    isSeller = BooleanField('Add Seller Functionality')
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data,
                         form.isSeller.data
                         ):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


class ManageBalance(FlaskForm):
    amount = StringField('Amount to Withdraw', validators=[DataRequired()])
    amount2 = StringField('Amount to Deposit', validators=[DataRequired()])
    submit = SubmitField('Complete Transaction')


@bp.route('/manage_balance', methods=['GET', 'POST'])
def manage_balance():
    if current_user.is_authenticated:
        curr_id = current_user.id
        form = ManageBalance()
        if form.validate_on_submit:
            amount_to_withdraw = form.amount.data
            amount_to_deposit = form.amount2.data
            if amount_to_withdraw is not None:
                out = current_user.withdraw(curr_id, amount_to_withdraw)
                if out is None:
                    flash('You do not have sufficient funds in your account to withdraw this amount!')
                    return redirect(url_for('users.manage_balance'))
                elif out:
                    flash('Congratulations, your transaction was successful!')
                    return render_template('account.html', current_user=current_user)   
            if amount_to_deposit is not None:
                out = current_user.deposit(curr_id, amount_to_deposit)
                if out:
                    flash('Congratulations, your transaction was successful!')
                    return render_template('account.html', current_user=current_user)           
    return render_template('manageBalance.html', form=form)

@bp.route('/update_account', methods=['GET', 'POST'])
def update_account_details():
    if current_user.is_authenticated:
        user_details = current_user.user_details
        print(user_details)
        if request.method == 'POST':
            updated_values_dict = request.form.to_dict()
            print(updated_values_dict)
            for k, v in updated_values_dict.items():
                if k == 'update_name_first':
                    new_first = v.rstrip()
                    if new_first == '':
                        new_first = None
                if k == 'update_name_last':
                    new_last = v.rstrip()
                    if new_last == '':
                        new_last = None
                if k == 'update_email':
                    new_email = v.rstrip()
                    if new_email == '':
                        new_email = None
            if User.update_information(current_user, new_email, new_first, new_last):
                return render_template('account.html', current_user=current_user)
            else:
                return render_template('updateInfo.html', user_details=user_details)
    return render_template('updateInfo.html', user_details=user_details)
