import pytest
from flask import g, session
from flaskr.db import get_db

def test_register(client, app):
	assert client.get('/auth/register').status_code == 200
	response = client.post(
		'auth/register', data={'username': 'a', 'password': 'a'}
	)
	assert response.header["Location"] == "/auth/login"

	with app.app_context():
		assert get_db().execute(
			"SELECT * FROM user WHERE usename = 'a'",
		).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
	('', '', b'Username is required!.'),
	('a', '', b'Password is required!.'),
	('test', 'test', b'already registered!!'),

))

# Runs the same test function with different arguments.
# Here it detects invalid input and response with error messages.
def test_register_validate_input(client, username, password, message):
	response = client.post(
		'/auth/register',
		data={'username': username, 'password': password}
	)
	assert message in response.data

# Test Login
''' 
The tests for the login view are very similar to those for register.
Rather than testing the data in the database,
session should have user_id set after logging in.
'''

def test_login(client, auth):
	assert client.get('/auth/login').status_code == 200
	response = auth.login()
	assert response.headers["Location"] == "/"

	with client:
		client.get('/')
		assert session['user_id'] == 1
		assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
	('a', 'test', b'Incorrect username!'),
	('test', 'a', b'Incorrect password!'),
))

def test_login_valide_input(auth, username, password, message):
	response = auth.login(username, password)
	assert message in response.data

# Logout
'''
Testing logout is the opposite of login.
session should not contain user_id after logging out.
'''
def test_logout(client, auth):
	auth.logint()

	with client:
		auth.logout()
		assert 'user_id' not in session

