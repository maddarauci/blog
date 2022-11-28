# blog

developed on windows

---
To run the application, use the flask command or 'python -m flask'.
You need to tell Flask where your application is with '--app' option.

```
$ flask --app "filename" run
	* Serving Flask app 'hello'
	* Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

## Running the Tests:
> 1. To run the tests, use the pytest command.
It will find and run all the test functions.
```
$ pytest

========================= test session starts ==========================
platform linux -- Python 3.6.4, pytest-3.5.0, py-1.5.3, pluggy-0.6.0
rootdir: /home/user/Projects/flask-tutorial, inifile: setup.cfg
collected 23 items

test/test_auth.py ........                                      [ 34%]
test/test_blog.py ............                                  [ 86%]
test/test_db.py ..                                              [ 95%]
test/test_factory.py ..                                         [100%]

====================== 24 passed in 0.64 seconds =======================
```

If any tests fail, pytest will show the error that was raised. You can run pytest -v to get a list of each test function rather than dots.


To measure the code coverage of your tests, use the coverage command to run pytest instead of running it directly.

```
$ coverage run -m pytest
```
You can either view a simple coverage report in the terminal:

```
$ coverage report

Name                 Stmts   Miss Branch BrPart  Cover
------------------------------------------------------
flaskr/__init__.py      21      0      2      0   100%
flaskr/auth.py          54      0     22      0   100%
flaskr/blog.py          54      0     16      0   100%
flaskr/db.py            24      0      4      0   100%
------------------------------------------------------
TOTAL                  153      0     44      0   100%
```
An HTML report allows you to see which lines were covered in each file:

```
$ coverage html
```

This generates files in the htmlcov directory. Open htmlcov/index.html in your browser to see the report.
