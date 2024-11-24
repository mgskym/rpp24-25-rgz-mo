from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db import db
from db.models import users, operations, actions
from flask_login import login_user, login_required, current_user, logout_user
import time

app = Flask(__name__)

app.secret_key = '123'
user_db = "postgres"
host_ip = "localhost"
host_port = "5432"
database_name = "rpp_rgz_2024"
password = "postgres"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))


@app.route("/")
@app.route("/index")
@login_required
def start():
    return redirect("/list", code=302)


@app.route("/login", methods=['GET'])
def login():
    return render_template(
        'login.html'
    )


@app.route("/login", methods=['POST'])
def login_2():
    email_form = request.form.get('email')
    password_form = request.form.get('password')
    my_user = users.query.filter_by(email=email_form).first()
    if (email_form != '' and password_form != ''):
        if my_user:
            if check_password_hash(my_user.password, password_form):
                login_user(my_user, remember=False)
                return redirect("/index", code=302)
            else:
                errors = 'Неверный логин или пароль'
                return render_template(
                'login.html',
                errors=errors
            )
        else:
            errors = 'Пользователь с таким Email не найден'
            return render_template(
                'login.html',
                errors=errors
            )
    else:
        errors = 'Не заполнены все обязательные поля'
        return render_template(
            'login.html',
            errors=errors
        )


@app.route("/signup", methods=['GET'])
def register_get():
    return render_template(
        'signup.html'
    )


@app.route("/signup", methods=['POST'])
def register_post():
    username_form = request.form.get('username')
    email_form = request.form.get('email')
    password_form = request.form.get('password')
    errors = "Не заполнены все обязательные поля"

    is_user_exists = users.query.filter_by(email=email_form).first()

    if (username_form != '' and email_form != '' and password_form != ''):
        if is_user_exists:
            errors = 'Пользователь с такими данными уже существует'
            return render_template(
                'signup.html',
                errors=errors
            )
        else:
            hashedPswd = generate_password_hash(password_form, method="pbkdf2")
            newUser = users(
                username = username_form,
                email = email_form,
                password = hashedPswd
            )
            db.session.add(newUser)
            db.session.commit()
            return redirect("/login", code=302)
    else:
        errors = 'Не заполнены все обязательные поля'
        return render_template(
                'signup.html',
                errors=errors
        )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/add", methods=['POST'])
# @login_required
def operations_adding():
    user_id_form = request.args['user_id']
    amount_form = request.args['amount']
    category_form = request.args['category']
    description_form = request.args['description']
    created_at_form = request.args['created_at']

    newOperation = operations(
                user_id = user_id_form,
                amount = amount_form,
                category = category_form,
                description = description_form,
                created_at = created_at_form
            )
    db.session.add(newOperation)
    db.session.commit()
    return make_response(200, 'OK')


@app.route("/list", methods=['GET'])
@login_required
def operations_list():
    user_operations = operations.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'index.html',
        operations = user_operations
    )
