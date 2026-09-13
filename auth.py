import functools
import sqlite3
from flask import (
    Blueprint, render_template, request, redirect, url_for, session, flash, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db


bp = Blueprint('auth', __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if g.get('user') is None:
            flash('Please log in to access your account.', 'error')
            return redirect(url_for('auth.login', next=request.path))
        return view(*args, **kwargs)
    return wrapped

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()

@bp.route("/register", methods=('GET', 'POST'))
def register():
    if g.user:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        password2 = request.form.get("password2", "").strip()
        error = None
        if not username or not password:
            error = 'Please enter a username and password.'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters long.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters long.'
        elif password != password2:
            error = 'Passwords do not match.'
        
        if error is None:
            db = get_db()
            try:
                cur = db.execute(
                    'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
                db.execute(
                    "INSERT INTO profiles (user_id) VALUES (?)", (cur.lastrowid,)
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = f'Username "{username}" is already taken.'
            else:
                flash('Account created successfully! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
        flash(str(error), 'error')
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        error = None
        if user is None or not check_password_hash(user['password_hash'], password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            next_url = request.args.get('next')
            return redirect(next_url or url_for('dashboard'))
        flash(error, 'error')
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('landing'))