from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from model import User
from database import db
import re

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validate mobile number
        """
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            flash("Enter a valid 10-digit mobile number.", "danger")
            return redirect(url_for('auth.signup'))"""

        # Check if password is strong
        if not is_valid_password(password):
            flash("Password must be at least 8 characters long and include letters, numbers, and special characters.", "danger")
            return redirect(url_for('auth.signup'))

        # Check if user exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already taken. Please try a different one.", "danger")
            return redirect(url_for('auth.signup'))

        # Hash password and create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Store user info in session
        session['username'] = username
        session['email'] = email
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        # Check if user credentials are valid
        if user and check_password_hash(user.password, password):
            session['id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            #session['mobile'] = user.mobile_number
            return redirect(url_for('auth.profile'))
        else:
            flash("Login failed. Please check your username and password.", "danger")

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('views.home'))

def is_valid_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Za-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )
@auth.route('/profile')
def profile():
    if "id" not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.get(session["id"])  # Fetch user from DB using session ID
    if not user:
        return redirect(url_for('auth.login'))

    return render_template("profile.html", user=user)
