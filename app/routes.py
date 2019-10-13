# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, request, session, flash, make_response
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db, dropzone
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.generate import update_csv, load_model
import codecs
from csv import reader
import json
import stripe
from werkzeug.wrappers import Response


# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            print("Both fields required")
            return json.dumps({'status': 'Both fields required'})
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            print("Invalid username or password")
            return json.dumps({'status': 'Invalid username or password'})
        login_user(user, remember=True)
        print("Successfully logged in")
        return json.dumps({'status': 'Successfully logged in'})
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    print("Succesfully logged out")
    return redirect(url_for('home'))


# -------- Signin Page ---------------------------------------------------------- #
@app.route('/register', methods=['GET', 'POST'])
def register():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form["email"]
        if not username or not password or not email:
            print("All fields required")
            return json.dumps({'status': 'All fields required'})
        if not User.query.filter_by(username=username).first() is None:
            print("Username taken")
            return json.dumps({'status': 'Username taken'})
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        print("Successfully registered")
        return json.dumps({'status': 'Successfully registered'})
    return render_template("register.html", title="Register", form=form)


# -------- Settings Page ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return "This route is under construction"


# -------- Home page ---------------------------------------------------------- #
@app.route("/")
@app.route("/main")
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# -------- Subscribe page (stripe)---------------------------------------------------------- #


@app.route("/sub")
@app.route("/subscribe", methods=['GET', 'POST'])
@login_required
def subscribe():
    if current_user.is_subscribed:
        return redirect(url_for("home"))
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]
    buy = stripe.checkout.Session.create(
        payment_method_types=['card'],
        subscription_data={
            'items': [{
                'plan': app.config["STRIPE_PLAN_ID"],
            }],
        },
        success_url='http://localhost:5000/success',
        cancel_url='http://localhost:5000/cancel',
    )
    _id = buy.get("id")
    current_user.session_id = _id
    db.session.commit()
    return render_template('subscribe.html', _id=_id, stripe_public_key=app.config["STRIPE_PUBLIC_KEY"], user=current_user)


# -------- Subscription Succes Page ---------------------------------------------------------- #
@app.route('/success')
@login_required
def success():
    current_user.subscription_id = stripe.checkout.Session.retrieve(current_user.session_id).subscription
    db.session.commit()
    status = stripe.Subscription.retrieve(current_user.subscription_id).status
    if status == "active":
        current_user.is_subscribed = True
        db.session.commit()
    return render_template('success.html')

# -------- Subscription Cancel page ---------------------------------------------------------- #


@app.route('/cancel')
@login_required
def cancel():
    return "CANCELED"


#---------- Dropzone -------------------------------------------------------------------------
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.is_subscribed:
        try:
            response = response
        except:
            response = None
        model = load_model()
        if request.method == 'POST':
            for key, file in request.files.items():
                if key.startswith('file'):
                    csvfile = update_csv(model=model, file=list(reader(codecs.iterdecode(file, 'utf-8-sig'), delimiter=";")))
                    #---------- Get updated csv file with predictions
                    response = json.dumps({'file': csvfile})
                    print("Sending response:")
                    print(response)
                    return response
        print(response)
        return render_template('upload.html', response=response)
    return redirect(url_for("index"))
