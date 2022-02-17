from flask import Flask
from recipe_app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Создание объекта приложения
app = Flask(__name__)
# Ввод конфиг файла для приложения
app.config.from_object(Config)

# Подключение готовой базы данных
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

# Настройка пользовательского входа с помощь логин менеджера
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Пожалуйста, выполните вход для дальнейших действий'

# Подключени шифратора паролей
bcrypt = Bcrypt(app)

# Подключение узлов с методами к приложению
# from app.module import route
from  recipe_app.identification.identification import identification
from recipe_app.profile_page.profile_page import profile
from recipe_app.recipe_page.recipe_page import recipe

# app.register_blueprint(route)
app.register_blueprint(identification)
app.register_blueprint(profile)
app.register_blueprint(recipe)
