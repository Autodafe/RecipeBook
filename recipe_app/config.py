class Config:
    # Данные конфигурации подключения к БД
    dialect = 'postgresql'
    username = 'vhreypnmdgorcg'
    password = '2180c86ea96dd86a268846a2dda3ebd56654123ed12549dfbfc1ca30e0a6ccf6'
    host = 'ec2-54-158-26-89.compute-1.amazonaws.com'
    db_name = 'ddunej9gqkblss'

    # Настройки для экземляра: секретный ключ запуска и путь к БД
    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dfwqoi1231mewqkoq12k6podwaspo'
