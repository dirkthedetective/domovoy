import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import urllib
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import pandas as pd

def create_app(test_config=None):
    
    
    # Создать приложение
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.static_folder = 'static'

    # Создать базу данных SQL 
    # params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-UF0F83M;DATABASE=STREAMINGDB;Trusted_Connection=yes;')
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
    # app.config['SECRET KEY'] = 'dev'

    # db = SQLAlchemy(app)
    # bcrypt = Bcrypt(app)

    # if test_config is None:
    #    app.config.from_pyfile('config.py', silent=True)
    # else:
    #    app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        return render_template("index.html")
    
    return app