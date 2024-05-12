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
import datetime

def create_app(test_config=None):
    
    
    # Создать приложение
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.static_folder = 'static'

    # Создать базу данных SQL 
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-UF0F83M;DATABASE=DOMOVOYDB;Trusted_Connection=yes;')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
    app.config['SECRET KEY'] = 'dev'

    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    class Blog_Entry(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        author_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

        text = db.Column(db.Text, nullable=False)

        creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

        image_link = db.Column(db.String(300))

        role2 = db.relationship('User',
        backref=db.backref('blog_entry', lazy=True))

        def __repr__(self):
            return '<Blog_Entry %r>' % self.id
        
    class Order_Document(db.Model):
        order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
        document_id = db.Column(db.Integer, db.ForeignKey('document.id'), primary_key=True)
        #client_id = db.Column(db.Integer, primary_key=True)
        #author_id = db.Column(db.Integer, primary_key=True)
        #design_id = db.Column(db.Integer, primary_key=True)
        #fk = db.ForeignKeyConstraint(
        #    ["order_id", "client_id", "design_id"], ["order.id", "order.client_id", "order.design_id"]
        #)
        #fk2 = db.ForeignKeyConstraint(
        #    ["document_id", "author_id"], ["document.id", "document.author_id"]
        #)

        name = db.Column(db.String(80), primary_key=True)

        role = db.relationship("Order", 
        backref=db.backref('order_document', lazy=True))

        def __repr__(self):
            return '<Order_Document %r>' % self.name

    class Design_Document(db.Model):
        design_id = db.Column(db.Integer, db.ForeignKey('design.id'), primary_key=True)
        document_id = db.Column(db.Integer, db.ForeignKey('document.id'), primary_key=True)
        #client_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), primary_key=True)
        #fk = db.ForeignKeyConstraint(
        #    ["document_id", "client_id"], ["document.id", "document.author.id"]
        #)

        def __repr__(self):
            return '<Design_Document %r>' % self.name

    class Order(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)
        client_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
        design_id = db.Column(db.Integer, db.ForeignKey('design.id'), primary_key=True)

        creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
        finish_date = db.Column(db.DateTime)

        role = db.relationship('User',
        backref=db.backref('order', lazy=True))
        
        order_status = db.Column(db.String(20), default="Pending")
        def __repr__(self):
            return '<Order %r>' % self.order_status

    class Document(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)
        author_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

        creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
        document_type = db.Column(db.String(20))
        document_link = db.Column(db.String(300))
 
        role = db.relationship('Order_Document',        
        backref=db.backref('document', lazy=True))
        role2 = db.relationship('Design_Document',
        backref=db.backref('document', lazy=True))
        
        role3 = db.relationship('User',
        backref=db.backref('document', lazy=True))

        def __repr__(self):
            return '<Document %r>' % self.id

    # Класс пользователя
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        username = db.Column(db.String(20), nullable=False, unique=True)
        password = db.Column(db.String(80), nullable=False)

        first_name = db.Column(db.String(20), nullable=False)
        last_name = db.Column(db.String(20))

        phone_number = db.Column(db.Integer)
        account_type = db.Column(db.String(20))

        def __repr__(self):
            return '<User %r>' % self.username

    class Design(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)

        title = db.Column(db.String(20), nullable=False)
        description = db.Column(db.String(20), nullable=False)
        price = db.Column(db.Integer)

        image_link = db.Column(db.String(300))

        role = db.relationship('Design_Document',
        backref=db.backref('design', lazy=True))
        role2 = db.relationship('Order',
        backref=db.backref('design', lazy=True))

        def __repr__(self):
            return '<Design %r>' % self.title
   
    with app.app_context():
        db.create_all()

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        return render_template("index.html")
    
    @app.route('/user/<id>')
    def user(id):
        user = db.one_or_404(db.select(User).filter_by(id=1))
        return render_template("user.html", user = user)
    
    return app