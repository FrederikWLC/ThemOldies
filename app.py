# -*- coding: utf-8 -*-
import stripe
from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import os
from settings import stripe_plan_id, stripe_public_key, stripe_secret_key
app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
stripe.api_key = stripe_secret_key


# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    return render_template('home.html', user=user)


@app.route("/logout")
def logout():
    session['logged_in'] = False
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
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings Page ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
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
    if session.get('logged_in'):
        user = helpers.get_user()
        return render_template("home.html", user=user)
    return render_template("home.html")

# -------- Subscribe page (stripe)---------------------------------------------------------- #


@app.route("/sub")
@app.route("/subscribe", methods=['GET', 'POST'])
def subscribe():
    if session.get('logged_in'):
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
        user.subscription = True
        return render_template('subscribe.html', _id=_id, stripe_public_key=stripe_public_key, user=user)
    return redirect(url_for('login'))
# -------- Subscription Succes Page ---------------------------------------------------------- #


@app.route('/success')
def success():
    return render_template('success.html')

# -------- Subscription Cancel page ---------------------------------------------------------- #


@app.route('/cancel')
def cancel():
    return "CANCELED!"


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
