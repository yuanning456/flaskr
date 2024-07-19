from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from rag import bp as rag_bp
import os
import logging
from dotenv import load_dotenv


# 加载 .env 文件
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.register_blueprint(rag_bp, url_prefix='/rag')

log_path = os.path.join(os.getcwd(), 'logs', 'application.log')

# 配置日志处理器
handler = logging.FileHandler(log_path, encoding='utf-8')
handler.setLevel(logging.DEBUG)  # 设置日志级别
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.logger.error('Application started')



















class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        flash('Login successful')
        return redirect(url_for('user_home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
def index():
    return 'Welcome to the Home Page!'

@app.route('/user')
def user_home():
    return 'Welcome to your user home page!'

@app.route('/add_user', methods=['POST'])
def add_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('user_home'))
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




