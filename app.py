from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db import db
from db.models import users, operations, actions
from flask_login import login_user, login_required, current_user, logout_user
from datetime_calculation import current_datetime_sql
import json
import os

app = Flask(__name__)

app.secret_key = os.environ.get('APP_SECRET_KEY')
user_db = os.environ.get('USER_DB')
host_ip = "localhost"
host_port = "5432"
database_name = os.environ.get('DATABASE_NAME')
password = os.environ.get('PASSWORD')

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
    if (email_form and password_form):
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

    if (username_form and email_form and password_form):
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


@app.route("/add", methods=['GET'])
@login_required
def operations_adding_page():
    return render_template(
        "add.html"
    )


@app.route("/add", methods=['POST'])
@login_required
def operations_adding():
    amount_form = request.form.get('amount')
    category_form = request.form.get('category')
    description_form = request.form.get('description')
    if (amount_form and category_form):
        newOperation = operations(
                    user_id = current_user.id,
                    amount = amount_form,
                    category = category_form,
                    description = description_form,
                    created_at = current_datetime_sql()
                )
        db.session.add(newOperation)
        db.session.commit()

        operation_id = (operations.query.filter_by(user_id=current_user.id, amount=amount_form, created_at=current_datetime_sql()).first()).id
        newAction = actions(
            operation_id = operation_id,
            action_type = 'Добавление',
            date = current_datetime_sql()
        )
        db.session.add(newAction)
        db.session.commit()
        
        message = f'Операция на сумму {amount_form} руб. успешно добавлена'
        return render_template(
            "add.html",
            message=message
        )
    else:
        errors = f'Поля "Сумма" и "Категория" обязательны для заполнения'
        return render_template(
            "add.html",
            errors=errors
        )


@app.route("/list", methods=['GET'])
@login_required
def operations_list():
    user_operations = operations.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'index.html',
        operations = user_operations
    )


@app.route("/delete", methods=['POST'])
@login_required
def delete_operation():
    operation_id = request.get_json(force=True)['id']
    operation = operations.query.filter_by(id=operation_id).first()

    newAction = actions(
            operation_id = operation_id,
            action_type = 'Удаление',
            date = current_datetime_sql()
        )
    db.session.add(newAction)
    db.session.commit()

    db.session.delete(operation)
    db.session.commit()
    return make_response('OK')


@app.route("/edit", methods = ['POST', 'GET'])
@login_required
def edit_redirect():
    id_edit = request.form.get("selected_operation")
    operations_all = operations.query.filter_by(user_id=current_user.id).all()
    if request.method == 'GET':
        return render_template(
            '/edit_select.html',
            operations = operations_all
        )
    else:
        return redirect(f'/edit/{id_edit}')


@app.route("/edit/<string:id_edit>", methods = ['POST', 'GET'])
@login_required
def edit_operation_post(id_edit):
    operation = operations.query.filter_by(id=id_edit).first()
    if request.method == 'GET':
        return render_template(
        "edit.html",
        operation=operation
    )
    else:
        if (amount_form and category_form):
            operation = operations.query.filter_by(id=id_edit).first()
            amount_form = request.form.get('amount')
            category_form = request.form.get('category')
            description_form = request.form.get('description')

            operation.amount = amount_form
            operation.category = category_form
            operation.description = description_form
            db.session.commit()

            newAction = actions(
                operation_id = operation.id,
                action_type = 'Редактирование',
                date = current_datetime_sql()
            )
            db.session.add(newAction)
            db.session.commit()

            message = f'Изменения сохранены'
            return render_template(
                "edit.html",
                operation=operation,
                message=message
            )
        else:
            errors = f'Поля "Сумма" и "Категория" обязательны для заполнения'
            return render_template(
                "edit.html",
                operation=operation,
                errors=errors
            )