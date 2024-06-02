import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import urllib
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DecimalField, FileField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt
import pandas as pd
import datetime
import jsonpickle

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
    
        # Формы для регистрации ------------------------------------------------------
    class RegisterForm(FlaskForm):
        username = StringField(validators=[
                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Имя пользователя"})

        password = PasswordField(validators=[
                            InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Пароль"})
                
        first_name = StringField(validators=[
            InputRequired()], render_kw={"placeholder": "Имя"})

        last_name = StringField(render_kw={"placeholder": "Фамилия"})
        phone_number = IntegerField(render_kw={"placeholder": "Номер телефона"})

        submit = SubmitField('Зарегистрируйтесь')

        def validate_username(self, username):
            existing_user_username = User.query.filter_by(
                    username=username.data).first()
            if existing_user_username:
                raise ValidationError(
                    'That username already exists. Please choose a different one.')
                    
    class LoginForm(FlaskForm):
        username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Имя пользователя"})

        password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Пароль"})

        submit = SubmitField('Войти')

    class DesignForm(FlaskForm):
        id = StringField(render_kw={"placeholder": "ID"})

        title = StringField(render_kw={"placeholder": "Название"})
        description = StringField(render_kw={"placeholder": "Описание"})
        price = IntegerField(render_kw={"placeholder": "Цена"})
        floor_count = IntegerField(render_kw={"placeholder": "Этажи"})
        area_size = DecimalField(render_kw={"placeholder": "Площадь"})
        material = StringField(render_kw={"placeholder": "Материал"})

        select = SelectField(choices=[("Insert", "Insert"), ("Update", "Update"), ("Delete", "Delete")], validators=[InputRequired()])

        submit = SubmitField('Submit')

    class DocumentUploadForm(FlaskForm):
        title = StringField('Title', validators=[DataRequired()])
        document_type = StringField('Document Type (optional)')
        file = FileField('Upload Document', validators=[DataRequired()])
        submit = SubmitField('Upload')

    class Blog_Entry(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        author_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

        title = db.Column(db.String(100), nullable=False)
        text = db.Column(db.Text, nullable=False)

        creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

        image_link = db.Column(db.Text)

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
         
        role2 = db.relationship('Document',        
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
        role = db.relationship("Design", 
        backref=db.backref('design_document', lazy=True))
        role2 = db.relationship('Document',
        backref=db.backref('design_document', lazy=True))

        def __repr__(self):
            return '<Design_Document %r>' % self.name

    class Order(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
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
        id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
        author_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

        title = db.Column(db.String(100), nullable=False)
        creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
        document_type = db.Column(db.String(20))
        document_link = db.Column(db.Text)

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
        id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)

        title = db.Column(db.String(20), nullable=False)
        description = db.Column(db.Text, nullable=False)
        price = db.Column(db.Integer)

        floor_count = db.Column(db.Integer)
        area_size = db.Column(db.Float)
        wall_material = db.Column(db.String(30))

        image_link = db.Column(db.Text)

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
        designs = Design.query.all()
        for design in designs:
            design_path = os.path.join(app.static_folder, f'designs/{design.id}')
            design.images = []  # Empty list to store image paths
            if os.path.isdir(design_path):  # Check if directory exists
                for filename in os.listdir(design_path):
                    if os.path.isfile(os.path.join(design_path, filename)):  # Check if file
                        design.images.append(url_for('static', filename=f'designs/{design.id}/{filename}'))
        return render_template("home.html", designs=designs)
    
    @app.route('/blog')
    def blog():
        entries = Blog_Entry.query.all()
        for entry in entries:
            author = User.query.filter_by(id=entry.author_id).first()
            entry.author = author.first_name + " " + author.last_name
            design_path = os.path.join(app.static_folder, f'blog/{entry.id}')
            entry.images = []  # Empty list to store image paths
            if os.path.isdir(design_path):  # Check if directory exists
                for filename in os.listdir(design_path):
                    if os.path.isfile(os.path.join(design_path, filename)):  # Check if file
                        entry.images.append(url_for('static', filename=f'blog/{entry.id}/{filename}'))
        return render_template("blog.html", entries=entries)
    
    @app.route('/user/<id>')
    def user(id):
        user = db.one_or_404(db.select(User).filter_by(id=id))
        return render_template("user.html", user = user)
    
    @app.route('/admin/documents', methods=['GET', 'POST'])
    def upload_document():
        form = DocumentUploadForm()
        if form.validate_on_submit():
            # Get user information (replace with your logic)

            # Get uploaded file
            uploaded_file = form.file.data

            # Generate filename (optional, replace with your logic)
            filename = uploaded_file.filename

            # Create a new document record
            new_document = Document(
                title=form.title.data,
                author_id=current_user.id,
                creation_date=datetime.datetime.now(),
                document_type=form.document_type.data,
                document_link=filename  # Update if storing filepath instead of link
            )

            # Add document to database and commit
            db.session.add(new_document)
             # Save the file (replace with your storage logic)
            uploaded_file.save(os.path.join(app.static_folder, f'documents/{filename}'))

            db.session.commit()

            # Flash message (optional)
            flash('Document uploaded successfully!', 'success')

            return redirect(url_for('upload_document'))
        
        docs = Document.query.all() 
        orders = Order.query.all()
        for order in orders:
            order.username = User.query.filter_by(id=order.client_id).first().username
        designs = Design.query.all() 
        return render_template('admin/documents.html', form=form, docs=docs, orders=orders, designs=designs)
    
    @app.route('/profile')
    @login_required
    def profile():
        orders = Order.query.filter_by(client_id=current_user.id).all()
        for order in orders:
            design = Design.query.filter_by(id=order.design_id).first()
            design_path = os.path.join(app.static_folder, f'designs/{design.id}')
            order.image = url_for('static', filename=f'designs/{design.id}/' + os.listdir(design_path)[0])
        return render_template("profile.html", orders=orders)
    
    @app.route('/catalogue')
    @login_required
    def catalogue():
        designs = Design.query.all()
        for design in designs:
            design_path = os.path.join(app.static_folder, f'designs/{design.id}')
            design.images = []  # Empty list to store image paths
            if os.path.isdir(design_path):  # Check if directory exists
                for filename in os.listdir(design_path):
                    if os.path.isfile(os.path.join(design_path, filename)):  # Check if file
                        design.images.append(url_for('static', filename=f'designs/{design.id}/{filename}'))
        return render_template("designs.html", designs=designs)
        
    @app.route('/design/<id>')
    def film(id):
        design = db.one_or_404(db.select(Design).filter_by(id=id))
        design_path = os.path.join(app.static_folder, f'designs/{design.id}')
        design.images = []  # Empty list to store image paths
        if os.path.isdir(design_path):  # Check if directory exists
            for filename in os.listdir(design_path):
                if os.path.isfile(os.path.join(design_path, filename)):  # Check if file
                    design.images.append(url_for('static', filename=f'designs/{design.id}/{filename}'))
        return render_template("design.html", design=design)
    
    @app.route('/api/design/<id>')
    def design(id):
        design = db.one_or_404(db.select(Design).filter_by(id=id))
        design_path = os.path.join(app.static_folder, f'designs/{design.id}')
        design.images = []  # Empty list to store image paths
        if os.path.isdir(design_path):  # Check if directory exists
            for filename in os.listdir(design_path):
                if os.path.isfile(os.path.join(design_path, filename)):  # Check if file
                    design.images.append(url_for('static', filename=f'designs/{design.id}/{filename}'))
        return jsonpickle.encode(design)
    
    @app.route('/api/document/<id>', methods=['DELETE'])
    def delete_doc(id):
        me = db.one_or_404(db.select(Document).filter_by(id=id))
        if me != None:
            db.session.delete(me)
            os.remove(os.path.join(app.static_folder, f'documents/{me.document_link}'))
            db.session.commit()
        else:
            print("Error!")
            flash('Entry not found.')
        return jsonpickle.encode({'message': 'Document deleted successfully'})
    
    @app.route('/api/design_document', methods=['POST'])
    def link_design_doc():
        # Access data from request.json
        document_id = request.json.get('document_id')
        design_id = request.json.get('design_id')
        name = request.json.get('name')

        design_doc = Design_Document(
            design_id=design_id,
            document_id=document_id,
            name=name
        )

        db.session.add(design_doc)
        db.session.commit()

        return jsonpickle.encode({'message': 'Data received successfully!'})

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('profile'))
        return render_template('login.html', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password, first_name=form.first_name.data, last_name=form.last_name.data, phone_number=form.phone_number.data, account_type="Client")
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

        return render_template('register.html', form=form)
    
    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    @app.route('/admin/designs', methods=['GET', 'POST'])
    @login_required
    def adminfilms():
        form = DesignForm()
        if form.is_submitted():
            if form.select.data == "Insert":
                if form.title.data and form.description.data:
                    me = Design(
                        title=form.title.data, description=form.description.data, price=form.price.data, floor_count=form.floor_count.data, 
                        area_size=form.area_size.data, wall_material=form.material.data)
                    db.session.add(me)
                    db.session.commit()
                    flash('Успех!')
                else:
                    flash('Название и описание необходимы для добавления')
            elif form.select.data == "Update":
                if form.id.data:
                    me = Design.query.filter_by(id=int(form.id.data)).first()
                    if form.title.data:
                        me.title = form.title.data
                    if form.description.data:
                        me.description = form.description.data
                    if form.price.data:
                        me.price=form.price.data
                    if form.floor_count.data:
                        me.floor_count=form.floor_count.data
                    if form.area_size.data:
                        me.area_size=form.area_size.data 
                    if form.material.data:
                        me.wall_material=form.material.data
                    db.session.commit()
                else:
                    flash('ID is required for Update.')
            elif form.select.data == "Delete":
                if form.id.data:
                        me = Design.query.filter_by(id=int(form.id.data)).first()
                        if me != None:
                            db.session.delete(me)
                            db.session.commit()
                        else:
                            print("Error!")
                            flash('Entry not found.')
                else:
                    flash('ID is required for Delete.')
            else:
                print("Error!")
                flash('Wrong.')

        table = Design.query.all()    
        return render_template("admin/designs.html", table=table, form=form)
    
    return app