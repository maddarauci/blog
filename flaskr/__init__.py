#./flaskr/__init__.py
import os
from flask import Flask
import secrets

# locals:
# import db

# THE FACTORY:


def create_app(test_config=None):
	# crate and configure the app 
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping (
		SECRET_KEY='7c0e9d12ec39994f1161b8b06a33d0076518e80f4d52ca307c7ba813af25c93d',
		#SECRECT_KEY = secrets.token_hex(),
		DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing.
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in.
		#app.config.from_mapping(test_config)
		app.config.update(test_config)


	# ensure the instace folder exists.
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass


	# a simple page that says 'hello'
	@app.route('/hello')
	def hello():
		return 'hello world'

	from flaskr import db

	
	db.init_app(app)

	# blueprint register
	from flaskr import auth, blog 
	app.register_blueprint(auth.bp)
	app.register_blueprint(blog.bp)

	app.add_url_rule("/", endpoint="index")

	return app
