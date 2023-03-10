from flask import Flask, render_template, url_for, redirect, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:addyourpasswordhere@localhost/users'
app.config['SECRET_KEY'] = 'secret123'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(300))


class RegisterForm(FlaskForm):
    fullname = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "FullName"})
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            flash("This username already exists.")
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


class MessageForm(FlaskForm):
    message = TextAreaField(validators=[
    InputRequired(), Length(min=1, max=300)], render_kw={"placeholder": "Enter your message here"})
    submit = SubmitField('Submit')

@app.route('/')
def home():
    session.pop('_flashes', None)
    return render_template('index.html')

@app.route('/contact', methods=['GET','POST'])
@login_required
def contact():
    form = MessageForm()
    if request.method == 'POST':
        print("post")
        if form.validate_on_submit():
            current_user.message = form.message.data
            db.session.commit()
            flash("Message submitted successfully.")
            
    return render_template('contact.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('contact'))
            else:
                flash("Incorrect login. Please try again.")
        else:
            flash("No such User exists. Please try again.")
    return render_template('login.html', form=form)


@ app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(fullname=form.fullname.data,username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
