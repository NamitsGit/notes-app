from flask import Blueprint, redirect, render_template, request, flash, url_for
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint("auth", __name__)


# USER auths
# u - namit@email.com  p - Namit1234

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password! Try again.", category="error")
        else:
            flash("User doesn't exist! ", category="error")
    data = request.form
    print(data)
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash("Email already being used by existing user!", category="error")
        elif len(email) < 4:
            flash("Email too short! Please enter a valid email.", category= "error")
        elif len(first_name) < 2:
           flash("First name too short! Please enter a valid first name.", category= "error")
        elif len(last_name) < 2:
            flash("Last name too short! Please enter a valid last name.", category= "error")
        elif password1 != password2:
            flash("Passwords don't match! Please re-enter the passwords", category= "error")
        elif len(password1) < 7:
            flash("Length of password too short! Please choose a password with a minimum of 8 characters.", category= "error")
        else:
            new_user = User(email=email, first_name = first_name, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!", category="success")
            login_user(user, remember=True)
            return redirect(url_for('views.home'), user=new_user)
            
    return render_template("sign_up.html", user=current_user)