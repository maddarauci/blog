# blueprint

import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for

	)
#./flaskr/auth.py
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# view register
@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required!'
		elif not password:
			error = 'Password is required!'

		# after user provides username and password (create the account!)
		if error is None:
			try:
				db.execute(
					"INSERT INTO user (username, password) VALUES (?, ?)",
					(username, generate_password_hash(password)),
					)
				db.commit()
			except db.IntegrityError:
				error = f"User {username} is already registered."
			else:
				return redirect(url_for("auth.login"))
		flash(error)
	return render_template('auth/register.html')

# login
@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
			).fetchone()
		# if requested username does not match list of db names (must be incorrect!)
		if user is None:
			error = 'Incorrect username.'
		# otherwise you're password is incorrect.
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))

		flash(error)
	return render_template('auth/login.html')

# load session (only if user logged in before)
@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user_id = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id,)
			).fetchone()

# logout: remove the user id from session and return to main index page!
@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))


# Authentication Required: only if user wants to post and edit posts
def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		# if user if not alreadu logged in
		if g.user is None:
			# goto login page
			return redirect(url_for('auth.login'))
		return view(**kwargs)
	return wrapped_view


