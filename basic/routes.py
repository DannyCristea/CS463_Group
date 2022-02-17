from flask import render_template, request, session, redirect, url_for, flash, request
from basic import app, db, bcrypt, mail
from basic.forms import (ContactForm, SignupForm, LoginForm,RequestResetPasswordForm,
                        ResetPasswordForm)#import all the forms from forms.py
from basic.models import User #import all models database from models.py
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message

import json
import razorpay
client = razorpay.Client(auth=("rzp_test_MY9PBjGDSugUcd","Ws0z4aB2yMbJrIGIhZkgxLY5"))



########################### HTML Routes Pages ##############
#www.streamit.com
@app.route('/', methods = ['GET','POST'])
def index():
    #pass all these variable into index.html page
    return render_template('index.html' , title='Home')

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/my-stuff')
@login_required #let user know that needs login to access this page
def mystuff():
    return render_template('my-stuff.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #flash('You have been logged in!','success')
            return redirect(next_page) if next_page else redirect(url_for('login'))
        else:
            flash('Login unseccessful. Please check email and password','danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/sign-up', methods = ['GET','POST'])
def signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.username.data }, Your account has been created!','success')
        return redirect(url_for('subscription_plan'))
    return render_template('sign-up.html', form=form)


@app.route('/contact-us', methods = ['GET','POST'])
def contactus():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(subject=f'Mail from {form.name.data}', body=f'Name: {form.name.data}\n E-mail: {form.email.data}\n {form.comment.data}', sender='hoda_sanij@outlook.com', recipients=['hoda_sanij@outlook.com'])
        mail.send(msg)
        flash(f'Thank you for contacting us!\n your form submitted successfully {form.name.data } .','success')
        return redirect(url_for('contactus'))
    return render_template('contact-us.html', form=form)

@app.route('/movie')
def movie():
    #pass all these variable into movie.html page
    return render_template('movie.html' , title='Movies&TvShows')

@app.route('/js/main.js')
def main_js():
    return render_template('/js/main.js')

@app.route('/about-us')
def aboutus():
    return render_template('about-us.html')

@app.route('/plans')
def plans():
    return render_template('plans.html' , title='Plans')

@app.route('/purchase-plan', methods = ['POST'])
# @csrf.exempt
def purchaseplan():
    # import pdb; pdb.set_trace()
    plan_name = request.get_json()['plan-name']
    amount = None
    if plan_name == 'standard':
        amount = 899
    elif plan_name == 'premium':
        amount = 1299
    elif plan_name == 'premium-plus':
        amount = 1699
    order_amount = amount
    order_currency = 'USD'
    order_receipt = 'order_rcptid_11'
    notes = {'Shipping address': 'Los Angeles, California'}   # OPTIONAL
    order=client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes))
    
    return json.dumps({'order-id':order['id'], 'order-amount': amount})


@app.route('/payment-handle', methods = ['POST'])
# @csrf.exempt
def paymenthandle():
    # import pdb; pdb.set_trace()
    plan_name = request.get_json()['plan_name']
    amount = request.get_json()['order_amount']
    razorpay_payment_id = request.get_json()['razorpay_payment_id']
    razorpay_order_id = request.get_json()['razorpay_order_id']
    razorpay_signature = request.get_json()['razorpay_signature']
    user = User.query.filter_by(email=current_user.email).first()
    payment = Payment(user_id=user.id, payment_id=razorpay_payment_id, order_id=razorpay_order_id, order_amount=amount, plan_name=plan_name)
    db.session.add(payment)
    db.session.commit()
    return json.dumps({'message':'success'})

@app.route('/finish-sign-up')
def subscription_plan():
    return render_template('finish-sign-up.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/base')#just for test
def mybase():
    return render_template('base.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='hoda_sanij@outlook.com',
                  recipients=['hoda_sanij@outlook.com'])
    #inorder to get the absolute URL not the Relative one we use _external
    msg.body =f'''Please Visit The Following Link To Reset Your Password:
{url_for('token_reset', token=token, _external=True)}
If this email is not originally from you, just ignore it!
'''
    mail.send(msg)


@app.route('/reset_password', methods = ['GET','POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent.', 'info')
        return redirect(url_for('login'))
    return render_template('request_reset.html', title='Reset Password', form=form)

#here we can take the token
@app.route('/reset_password/<token>', methods = ['GET','POST'])
def token_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:# when token is not valid
        flash('That is an invalid or expired code', 'warning')
        return redirect(url_for('request_reset'))
    form = ResetPasswordForm()#when token is validate
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated!','success')
        return redirect(url_for('login'))
    return render_template('token_reset.html', title='Reset Password', form=form)
