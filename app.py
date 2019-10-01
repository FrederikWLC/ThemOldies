# -*- coding: utf-8 -*-
import stripe
from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session, flash
import json
import sys
import os
from settings import stripe_plan_id, stripe_public_key, stripe_secret_key
from flask_dropzone import Dropzone
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


app = Flask(__name__)
app.config['TESTING'] = False
app.config["LOGIN_DISABLED"] = False
login = LoginManager()
login.init_app(app)
login.login_view = "login"
dropzone = Dropzone(app)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
stripe.api_key = stripe_secret_key


# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user:
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    user = helper.get_user()
                    login(user, remember=True)
                    return redirect(url_for("home"))
                flash("Invalid username or password")
                print("Invalid username or password")
                return redirect(url_for("login"))
            flash("Both fields required")
            print("Both fields required")
            return redirect(url_for("login"))
        return render_template('login.html', form=form)
    user = helpers.get_user()
    return render_template('home.html', user=user)


@app.route("/logout")
@login_required
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('login'))


# -------- Signup Page ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    flash("Signup was succesful")
                    return redirect(url_for("home"))
                flash("Username taken")
                return redirect(url_for("signup"))
            flash("Username and password required")
            return redirect(url_for("signup"))
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings Page ---------------------------------------------------------- #

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# -------- Home page ---------------------------------------------------------- #

@app.route("/")
@app.route("/index")
@app.route("/main")
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# -------- Subscribe page (stripe)---------------------------------------------------------- #


@app.route("/sub")
@app.route("/subscribe", methods=['GET', 'POST'])
@login_required
def subscribe():

    buy = stripe.checkout.Session.create(
        payment_method_types=['card'],
        subscription_data={
            'items': [{
                'plan': stripe_plan_id,
            }],
        },
        success_url='http://localhost:5000/success',
        cancel_url='http://localhost:5000/cancel',
    )

    print(buy)
    print("+" * 42)
    _id = buy.get("id")
    print(_id)
    user = helpers.get_user()
    return render_template('subscribe.html', _id=_id, stripe_public_key=stripe_public_key, user=user)
# -------- Subscription Succes Page ---------------------------------------------------------- #


@app.route('/success')
@login_required
def success():
    user = helpers.get_user()
    user.subscription = True
    return render_template('success.html')

# -------- Subscription Cancel page ---------------------------------------------------------- #


@app.route('/cancel')
@login_required
def cancel():
    return "CANCELED!"


#---------- Dropzone -------------------------------------------------------------------------
@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if session.get('logged_in'):
        user = helpers.get_user()
        if user.subscription:
            if request.method == 'POST':
                for key, f in request.files.items():
                    if key.startswith('file'):
                        # Handling of .csv file
                        pass
            return render_template('upload.html')
        return redirect(url_for("subscribe"))
    return redirect(url_for("login"))



# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
