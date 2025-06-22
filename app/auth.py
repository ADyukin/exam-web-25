from functools import wraps
from flask import Blueprint, request, render_template, url_for, flash, redirect, current_app, abort
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from .repositories import UserRepository
from . import db
import hashlib

user_repository = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Авторизуйтесь для доступа к этому ресурсу.'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, user_id, login, last_name, first_name, middle_name, role_id, role_name):
        self.id = user_id
        self.login = login
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.role_id = role_id
        self.role_name = role_name

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if current_user.role_name not in roles:
                flash('У вас недостаточно прав для выполнения данного действия', 'danger')
                return redirect(url_for('events.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@login_manager.user_loader
def load_user(user_id):
    user = user_repository.get_by_id(user_id)
    if user is not None:
        return User(
            user['id'],
            user['login'],
            user['last_name'],
            user['first_name'],
            user['middle_name'],
            user['role_id'],
            user['role_name']
        )
    return None

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        remember_me = request.form.get('remember_me') == 'on'

        # Хешируем пароль
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = user_repository.get_by_login_and_password(login, password_hash)

        if user is not None:
            login_user(User(
                user['id'],
                user['login'],
                user['last_name'],
                user['first_name'],
                user['middle_name'],
                user['role_id'],
                user['role_name']
            ), remember=remember_me)
            next_url = request.args.get('next', url_for('events.index'))
            return redirect(next_url)

        flash('Невозможно аутентифицироваться с указанными логином и паролем', 'danger')
        return render_template('auth/login.html')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('events.index'))