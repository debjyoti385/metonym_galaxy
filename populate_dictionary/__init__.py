# coding=utf8


from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('config.py')

from populate_dictionary.views import *
