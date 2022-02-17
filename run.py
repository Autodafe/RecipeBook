# Получение объекта приложения
from recipe_app import app

# Основной метод запуска приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
