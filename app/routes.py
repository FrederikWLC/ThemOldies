# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, request, session, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
import json


# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        if not form.username.data or not form.password.data:
            flash("Both fields required")
            return json.dumps({'status': 'Both fields required'})
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return json.dumps({'status': 'Invalid username or password'})
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("index")
            return redirect(url_for("index"))
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('índex'))


# -------- Signin Page ---------------------------------------------------------- #
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a member of ThemOldies!')
        return redirect(url_for("login"))
    render_template("register.html", title="Register", form=form)


# -------- Settings Page ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return "This route is under construction"


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
                'plan': app.config[STRIPE_PLAN_ID],
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
    return render_template('subscribe.html', _id=_id, stripe_public_key=app.config["STRIPE_PUBLIC_KEY"], user=user)


# -------- Subscription Succes Page ---------------------------------------------------------- #
@app.route('/success')
@login_required
def success():
    current_user.subscription = True
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
    if current_user.is_authenticated:
        if current_user.subscription:
            if request.method == 'POST':
                for key, f in request.files.items():
                    if key.startswith('file'):
                        # Handling of .csv file
                        pass
            return render_template('upload.html')
        return redirect(url_for("index"))
    return redirect(url_for("login"))



# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
