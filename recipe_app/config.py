class Config:
    # Данные конфигурации подключения к БД
    dialect = 'postgresql'
    username = 'postgres'
    password = 'Qwerty7'
    host = 'localhost'
    db_name = 'recipe_book'

    # Настройки для экземляра: секретный ключ запуска и путь к БД
    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dfwqoi1231mewqkoq12k6podwaspo'
