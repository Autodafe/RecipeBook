from flask_login import UserMixin
from recipe_app import db
from recipe_app import bcrypt
from recipe_app import login_manager
from flask import flash


# Обязательный метод для получения текущего ID пользователя
@login_manager.user_loader
def load_user(user_id):
    return BookUser.query.get(int(user_id))


# Таблица с пользователями системы
class BookUser(db.Model, UserMixin):
    __tablename__ = 'book_user'
    __table_args__ = {'extend_existing': True}

    id_book_user = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(length=150), nullable=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_book_user

    # Получение пароля
    @property
    def unencrypted_password(self):
        return self.unencrypted_password

    # Шифрование пароля
    @unencrypted_password.setter
    def unencrypted_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Проверка пароля
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    # Получение информации о пользователе по логину
    @staticmethod
    def get_user_by_login(login):
        return BookUser.query.filter_by(login=login).first()

    # Получение информации о пользователе по логину с ролью
    @staticmethod
    def get_user_by_login_with_role(login):
        query = db.session.query(BookUser, RoleUser)
        query = query.join(RoleUser, RoleUser.id_role == BookUser.id_role)
        query = query.filter(BookUser.login == login)
        return query.first()

    # Получение информации о пользователе по фамилии
    @staticmethod
    def get_user_by_fio(fio):
        return BookUser.query.filter_by(fio=fio).first()

    # Изменение данных о пользователе
    @staticmethod
    def update_system_user(login, fio, email, photo):
        try:
            user_for_update = BookUser.get_user_by_login(login)

            user_for_update.fio = fio
            user_for_update.email = email
            user_for_update.photo = photo

            db.session.commit()
            flash("Пользователь был успешно изменён.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при измении пользователя. Повторите попытку.", category='danger')

    # Добавление нового пользователя
    @staticmethod
    def add_system_user(fio, email, login, password, id_role, photo=None):
        new_system_user = BookUser(fio=fio, email=email, login=login, unencrypted_password=password,
                                   id_role=id_role, photo=photo)

        try:
            db.session.add(new_system_user)
            db.session.commit()
            flash("Пользователь был успешно добавлен.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении пользователя. Повторите попытку.", category='danger')


# Таблица с ролями пользователей в системе
class RoleUser(db.Model):
    __tablename__ = 'role_user'
    __table_args__ = {'extend_existing': True}

    # Получение всего списка ролей
    @staticmethod
    def get_all_roles():
        return RoleUser.query.all()

    # Получение всего списка ролей
    @staticmethod
    def get_role_by_name(name_role):
        return RoleUser.query.filter_by(name_role=name_role).first()


# Таблица с любимыми рецептами - избранное
class Favorite(db.Model):
    __tablename__ = 'favorite'
    __table_args__ = {'extend_existing': True}

    # Получение всего списка избранных рецептов
    @staticmethod
    def get_favorite_by_id_user(id_book_user):
        return Favorite.query.filter_by(id_book_user=id_book_user).all()

    # Добавление рецепта в избранное пользователя
    @staticmethod
    def add_favorite(id_recipe, id_book_user):
        new_user_favorite = Favorite(id_recipe=id_recipe, id_book_user=id_book_user)
        try:
            db.session.add(new_user_favorite)
            db.session.commit()
            flash("Рецепт был успешно добавлен в избранное.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении рецепта в избранное. Возможно у вас уже есть "
                  "этот рецепт в избранном.", category='danger')

    # Удаление рецепта
    @staticmethod
    def del_favorite(id_book_user, id_recipe):
        Favorite.query.filter_by(id_book_user=id_book_user, id_recipe=id_recipe).delete()
        try:
            flash("Рецепт был успешно убран из избранного.", category='success')
            db.session.commit()
        except:
            flash("Произошла ошибка при удалении рецепта из списка избранных. Повторите попытку.", category='danger')
            db.session.rollback()


# Таблица с ингридиентами на выбор
class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    __table_args__ = {'extend_existing': True}

    # Получение списка всех игнредиентов в БД
    @staticmethod
    def get_all_ingredients():
        return Ingredient.query.all()

    # Получение ID ингредиента по имени
    @staticmethod
    def get_ingredient_by_name(name_ingredient):
        return Ingredient.query.filter_by(name_ingredient=name_ingredient).first()

    # Добавление ингрединта в базу
    @staticmethod
    def add_ingredient(name_ingredient):
        new_ingredient = Ingredient(name_ingredient=name_ingredient)
        try:
            db.session.add(new_ingredient)
            db.session.commit()
            flash("Новый ингредиент был успешно добавлен.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении нового ингредиента. Повторите попытку.", category='danger')

    # Удаление ингредиента из базы
    @staticmethod
    def del_ingredient(id_ingredient):
        Ingredient.query.filter_by(id_ingredient=id_ingredient).delete()
        try:
            flash("Ингредиент был успешно удалён.", category='success')
            db.session.commit()
        except:
            flash("Произошла ошибка при удалении игредиента. Повторите попытку.", category='danger')
            db.session.rollback()


# Таблица с ингридиентами в блюде
class IngredientInRecipe(db.Model):
    __tablename__ = 'ingredient_in_recipe'
    __table_args__ = {'extend_existing': True}

    # Получение всех ингредиентов для рецепта
    @staticmethod
    def get_all_ingredients_for_recipe(id_recipe):
        query = db.session.query(IngredientInRecipe, Ingredient)
        query = query.join(Ingredient, Ingredient.id_ingredient == IngredientInRecipe.id_ingredient)
        query = query.filter(IngredientInRecipe.id_recipe == id_recipe)
        return query.all()

    # Добавление публикации рецепта пользователю
    @staticmethod
    def add_ingredient_for_recipe(id_recipe, id_ingredient, weight):
        new_ingredient_for_recipe = IngredientInRecipe(id_recipe=id_recipe, id_ingredient=id_ingredient, weight=weight)
        try:
            db.session.add(new_ingredient_for_recipe)
            db.session.commit()
            flash("Новый ингредиент был добавлен в рецепт.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении нового ингредиента в рецепт. Повторите попытку.", category='danger')


# Таблица с владельцами рецептов
class Publication(db.Model):
    __tablename__ = 'publication'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_id_of_personal_recipe_user(id_recipe):
        query = Publication.query.filter_by(id_recipe=id_recipe).first()
        return query.id_book_user

    @staticmethod
    def get_personal_recipes(id_book_user):
        query = db.session.query(Publication, Recipe, RecipeCategory)
        query = query.join(Recipe, Recipe.id_recipe == Publication.id_recipe)
        query = query.join(RecipeCategory, Recipe.id_category == RecipeCategory.id_category)
        query = query.filter(Publication.id_book_user == id_book_user)
        return query.all()

    # Добавление публикации рецепта пользователю
    @staticmethod
    def add_recipe_to_user(id_recipe, id_book_user):
        new_recipe_to_user = Publication(id_recipe=id_recipe, id_book_user=id_book_user)
        try:
            db.session.add(new_recipe_to_user)
            db.session.commit()
            flash("Новый рецепт был успешно опубликован.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при публикации нового рецепта. Повторите попытку.", category='danger')


# Таблица со всеми рецептами
class Recipe(db.Model):
    __tablename__ = 'recipe'
    __table_args__ = {'extend_existing': True}

    # Получение списка всех рецептов
    @staticmethod
    def get_recipes_by_name(recipe_name):
        return Recipe.query.filter_by(recipe_name=recipe_name).first()

    # Получение списка всех рецептов
    @staticmethod
    def get_all_recipes():
        query = db.session.query(Recipe, RecipeCategory)
        query = query.join(RecipeCategory, RecipeCategory.id_category == Recipe.id_category)
        return query.all()

    # Получение списка всех рецептов
    @staticmethod
    def get_all_favorite_recipes(id_book_user):
        query = db.session.query(Recipe, RecipeCategory, Favorite, BookUser)
        query = query.join(RecipeCategory, RecipeCategory.id_category == Recipe.id_category)
        query = query.join(Favorite, Favorite.id_recipe == Recipe.id_recipe)
        query = query.join(BookUser, BookUser.id_book_user == Favorite.id_book_user)
        query = query.filter(BookUser.id_book_user == id_book_user)
        return query.all()

    # Получение списка всех рецептов с привязкой к рецепту
    @staticmethod
    def get_recipe_by_id_with_category(id_recipe):
        query = db.session.query(Recipe, RecipeCategory)
        query = query.join(RecipeCategory, RecipeCategory.id_category == Recipe.id_category)
        query = query.filter(Recipe.id_recipe == id_recipe)
        return query.first()

    # Добавление нового рецепта
    @staticmethod
    def add_recipe(recipe_name, description, date_publication, id_category, photo, number_of_servings):
        new_recipe = Recipe(recipe_name=recipe_name, description=description, date_publication=date_publication,
                            id_category=id_category, photo=photo, number_of_servings=number_of_servings)
        try:
            db.session.add(new_recipe)
            db.session.commit()
            flash("Новый рецепт был успешно добавлен.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при нового рецепта. Повторите попытку.", category='danger')

    # Удаление рецепта
    @staticmethod
    def del_recipe(id_recipe):
        Recipe.query.filter_by(id_recipe=id_recipe).delete()
        try:
            flash("Рецепт был успешно удалён.", category='success')
            db.session.commit()
        except:
            flash("Произошла ошибка при удалении рецепта. Повторите попытку.", category='danger')
            db.session.rollback()


# Таблица с категориями рецептов
class RecipeCategory(db.Model):
    __tablename__ = 'recipe_category'
    __table_args__ = {'extend_existing': True}

    # Получение списка всех категорий рецептов
    @staticmethod
    def get_all_category():
        return RecipeCategory.query.all()

    # Получение информации об ID категории по именованию категорииы
    @staticmethod
    def get_category_by_name(name_category):
        return RecipeCategory.query.filter_by(name_category=name_category).first()


# Таблица с отзывами о рецептах
class Review(db.Model):
    __tablename__ = 'review'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_review_by_id_book_user(id_book_user):
        query = db.session.query(Review, BookUser, Recipe)
        query = query.join(BookUser, Review.id_book_user == BookUser.id_book_user)
        query = query.join(Recipe, Recipe.id_recipe == Review.id_recipe)
        query = query.filter(Review.id_book_user == id_book_user)
        return query.all()

    # Получение информации о всех отзывах по ID рецепта
    @staticmethod
    def get_review_by_id_recipe(id_recipe):
        query = db.session.query(Review, BookUser)
        query = query.join(BookUser, Review.id_book_user == BookUser.id_book_user)
        query = query.filter(Review.id_recipe == id_recipe)
        return query.all()

    # Добавление нового комментария для рецепта
    @staticmethod
    def add_review(id_recipe, id_book_user, comment, grade):
        new_review = Review(id_recipe=id_recipe, id_book_user=id_book_user, grade=grade, comment=comment)
        try:
            db.session.add(new_review)
            db.session.commit()
            flash("Отзыв был успешно оставлен.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при публикации отзыва. Повторите попытку.", category='danger')

    @staticmethod
    def del_review(id_book_user, id_recipe):
        Review.query.filter_by(id_book_user=id_book_user, id_recipe=id_recipe).delete()
        try:
            flash("Отзыв был успешно удалён.", category='success')
            db.session.commit()
        except:
            flash("Произошла ошибка при удалении отзыва. Повторите попытку.", category='danger')
            db.session.rollback()
