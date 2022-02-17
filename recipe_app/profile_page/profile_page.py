from flask import render_template, Blueprint, redirect, url_for, session, flash
from recipe_app.models import BookUser, Review, Recipe, Favorite, Ingredient
from recipe_app.forms import UpdateUserProfile, DeleteComment, RecipeInfoById, DelFavorite, AddIngredient, DelIngredient
from flask_login import login_required, current_user

# Создание узла связанного с профилем и его изменением
profile = Blueprint('profile', __name__, template_folder="templates")


# Просмотр информации о пользователе
@profile.route('/profile_view', methods=['GET'])
@login_required
def profile_view():
    activated_user = BookUser.get_user_by_login_with_role(session['login'])
    return render_template('profile/user_profile.html', activated_user=activated_user)


# Обновление профиля пользователя
@profile.route('/update_profile_view', methods=['GET', 'POST'])
@login_required
def profile_update_view():
    # Форма для обновления профиля
    update_profile_form = UpdateUserProfile()
    # Получение текущей информации о пользователе
    activated_user = BookUser.get_user_by_login(session['login'])

    if update_profile_form.submit_update.data:
        # Проверка на введённые в форме данные

        # ФИО
        if update_profile_form.fio.data:
            fio = update_profile_form.fio.data
        else:
            fio = activated_user.fio
        # Дата рождения
        if update_profile_form.email.data:
            email = update_profile_form.email.data
        else:
            email = activated_user.email
        # Фото пользователя
        if update_profile_form.photo.data:
            photo = update_profile_form.photo.data
        else:
            photo = activated_user.photo

        # Обновление профиля пользователя
        BookUser.update_system_user(session['login'], fio, email, photo)

        return redirect(url_for('profile.profile_view'))

    return render_template('profile/update_user_profile.html', activated_user=activated_user,
                           update_profile_form=update_profile_form)


# Просмотр комментариев пользователя
@profile.route('/profile_view_comments', methods=['GET', 'POST'])
@login_required
def user_personal_comments():
    # Все отзывы пользователя
    all_comments = Review.get_review_by_id_book_user(current_user.get_id())
    # Форма удаления комментария
    del_form_recipe = DeleteComment()

    # Удаления отзыва
    if del_form_recipe.submit_del_coma.data:
        Review.del_review(current_user.get_id(), del_form_recipe.id_recipe.data)
        return redirect(url_for('profile.user_personal_comments'))

    return render_template('profile/personal_reviews.html', all_comments=all_comments, del_form_recipe=del_form_recipe)


# Просмотр избранных рецептов пользователя
@profile.route('/profile_view_favorite', methods=['GET', 'POST'])
@login_required
def user_personal_favorite():
    # Получение списка всех рецептов
    all_recipe = Recipe.get_all_favorite_recipes(current_user.get_id())
    # Подключение формы для перехода за большей информацией о рецептемаршруте
    info_about_recipe = RecipeInfoById()
    # Форма удаления рецепта из избранного
    del_form_favorite = DelFavorite()

    # Переход по форме "узнать больше"
    if info_about_recipe.submit_info.data:
        return redirect(url_for('recipe.one_recipe_page_view', id_recipe=info_about_recipe.id_recipe.data))

    # Удаление из избранных
    elif del_form_favorite.submit_del_fav.data:
        Favorite.del_favorite(current_user.get_id(), del_form_favorite.id_recipe.data)
        return redirect(url_for('profile.user_personal_favorite'))

    return render_template('profile/favorite_recipe.html', all_recipe=all_recipe, info_about_recipe=info_about_recipe,
                           del_form_favorite=del_form_favorite)


# Добавление и удаление ингредиентов
@profile.route('/profile_ingredient_view', methods=['GET', 'POST'])
@login_required
def view_profile_ingredient():
    # Получение списка всех рецептов
    all_ingredients = Ingredient.get_all_ingredients()

    # Форма добавления ингредиента
    add_form_ingredient = AddIngredient()

    # Форма удаления ингредиента
    del_form_ingredient = DelIngredient()

    # Переход по форме "узнать больше"
    if add_form_ingredient.submit_add_ingred.data:
        Ingredient.add_ingredient(add_form_ingredient.ingredient.data)
        return redirect(url_for('profile.view_profile_ingredient'))

    # Удаление из избранных
    elif del_form_ingredient.submit_del_ingred.data:
        if session['role'] == 2:
            Ingredient.del_ingredient(del_form_ingredient.id_ingredient.data)
            return redirect(url_for('profile.view_profile_ingredient'))
        else:
            flash("Вы не можете удалять ингредиенты, т.к. вы не администратор", category='danger')
            return redirect(url_for('profile.view_profile_ingredient'))

    return render_template('profile/add_ingredient.html', all_ingredients=all_ingredients,
                           add_form_ingredient=add_form_ingredient, del_form_ingredient=del_form_ingredient)
