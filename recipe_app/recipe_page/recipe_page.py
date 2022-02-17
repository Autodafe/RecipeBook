from flask import Blueprint, render_template, redirect, url_for, session, flash
from recipe_app.models import Recipe, RecipeCategory, IngredientInRecipe, Publication, Review, Favorite, Ingredient, \
    BookUser
from recipe_app.forms import RecipeInfoById, AddRecipeForm, DeleteRecipe, AddComment, AddFavorite
from recipe_app.forms import DeleteComment, AddIngredientInRecipe
from flask_login import login_required, current_user

recipe = Blueprint('recipe', __name__, template_folder="templates")


# Начальная страница сайта
@recipe.route('/')
@recipe.route('/main', methods=['GET', 'POST'])
def recipe_page_view():
    # Получение списка всех рецептов
    all_recipe = Recipe.get_all_recipes()
    # Подключение формы для перехода за большей информацией о рецептемаршруте
    info_about_recipe = RecipeInfoById()

    # Переход по форме "узнать больше"
    if info_about_recipe.submit_info.data:
        return redirect(url_for('recipe.one_recipe_page_view', id_recipe=info_about_recipe.id_recipe.data))

    return render_template('recipe/main.html', all_recipe=all_recipe, info_about_recipe=info_about_recipe)


@recipe.route('/recipe/<id_recipe>', methods=['GET', 'POST'])
def one_recipe_page_view(id_recipe):
    # Получение информации о текущем рецепте
    recipe_for_view = Recipe.get_recipe_by_id_with_category(id_recipe)
    # Вывод всех ингредиентов рецепта
    ingredients_in_recipe = IngredientInRecipe.get_all_ingredients_for_recipe(id_recipe)
    # Форма для добавления комментария
    add_comment = AddComment()
    # Список всех комментариев для определённого рецепта
    all_comments = Review.get_review_by_id_recipe(id_recipe)
    # Форма добавления рецепта в избранное
    add_favorite = AddFavorite()
    # Форма удаления рецепта
    delete_recipe = DeleteRecipe()
    # Форма добавления ингредиента
    add_ingredient_form = AddIngredientInRecipe()
    # Получения списка всех ингредиентов
    all_ingredients = Ingredient.get_all_ingredients()
    # Заполнение списка ингредиентов
    add_ingredient_form.ingredient.choices = [i.name_ingredient for i in all_ingredients]
    # Получение ID владельца рецепта
    owner = Publication.get_id_of_personal_recipe_user(id_recipe)
    # Форма для удаление отзывов
    delete_comments = DeleteComment()

    if add_comment.submit_add.data:
        # Добавления отзыва
        Review.add_review(add_comment.id_recipe.data, current_user.get_id(), add_comment.comment.data,
                          add_comment.rate.data)
        return redirect(url_for('recipe.one_recipe_page_view', id_recipe=id_recipe))

    elif add_favorite.submit_add_fav.data:
        # Добавление рецепта в избранные
        Favorite.add_favorite(add_favorite.id_recipe.data, current_user.get_id())
        return redirect(url_for('recipe.one_recipe_page_view', id_recipe=id_recipe))

    elif delete_recipe.submit_del.data:
        if session['role'] == 2:
            # Удаление рецепта
            Recipe.del_recipe(delete_recipe.id_recipe.data)
            return redirect(url_for('recipe.recipe_page_view'))
        else:
            flash("Это может делать только админ", category='danger')
            return redirect(url_for('recipe.one_recipe_page_view', id_recipe=id_recipe))

    # Добавление нового ингредиента в рецепт
    elif add_ingredient_form.submit_add_ingro.data:
        if current_user.get_id() == owner:
            ingredient_for_add = Ingredient.get_ingredient_by_name(add_ingredient_form.ingredient.data)
            IngredientInRecipe.add_ingredient_for_recipe(id_recipe, ingredient_for_add.id_ingredient,
                                                         add_ingredient_form.weight.data)
            return redirect(url_for('recipe.one_recipe_page_view', id_recipe=id_recipe))
        else:
            flash("Вы должны быть владельцем рецепта", category='danger')
            return redirect(url_for('recipe.one_recipe_page_view', id_recipe=id_recipe))

    # Удаление отзыва админом
    elif delete_comments.submit_del_coma.data:
        if session['role'] == 2:
            search_user = BookUser.get_user_by_login(delete_comments.login_user.data)
            Review.del_review(search_user.id_book_user, id_recipe)
            return redirect(url_for('recipe.one_recipe_page_view', id_recipe=id_recipe))
        else:
            flash("Вы должны быть администратором", category='danger')
            return redirect(url_for('recipe.one_recipe_page_view', id_recipe=id_recipe))

    return render_template('recipe/one_recipe.html', recipe_for_view=recipe_for_view, all_comments=all_comments,
                           ingredients_in_recipe=ingredients_in_recipe, add_comment=add_comment,
                           add_favorite=add_favorite, id_recipe=id_recipe, delete_recipe=delete_recipe,
                           add_ingredient_form=add_ingredient_form, owner=owner, delete_comments=delete_comments)


@recipe.route('/personal_recipes', methods=['GET', 'POST'])
@login_required
def personal_recipe_view():
    # Получение информации о всех рецептах по ID пользователя
    all_recipe = Publication.get_personal_recipes(current_user.get_id())

    # Форма удаления рецепта
    del_recipe_form = DeleteRecipe()

    # Удаление рецепта - активация
    if del_recipe_form.submit_del.data:
        Recipe.del_recipe(del_recipe_form.id_recipe.data)
        return redirect(url_for('recipe.personal_recipe_view'))

    return render_template('recipe/view_personal_recipe.html', all_recipe=all_recipe,
                           del_recipe_form=del_recipe_form)


@recipe.route('/add_personal_recipe', methods=['GET', 'POST'])
@login_required
def personal_recipe_add():
    # Форма для добавления рецепта
    add_recipe_form = AddRecipeForm()

    # Заполнение категории рецепта
    add_recipe_form.category.choices = [i.name_category for i in RecipeCategory.get_all_category()]

    if add_recipe_form.submit_add.data:
        # Поиск ID категории блюда
        category_for_add = RecipeCategory.get_category_by_name(add_recipe_form.category.data)
        # Добавление нового рецепта
        Recipe.add_recipe(add_recipe_form.recipe_name.data, add_recipe_form.description.data,
                          add_recipe_form.date_publication.data, category_for_add.id_category,
                          add_recipe_form.photo.data, add_recipe_form.number_of_servings.data)
        # Публикация нового рецепта
        new_recipe = Recipe.get_recipes_by_name(add_recipe_form.recipe_name.data)
        Publication.add_recipe_to_user(new_recipe.id_recipe, current_user.get_id())

        return redirect(url_for('recipe.personal_recipe_view'))

    return render_template('recipe/add_personal_recipe.html', add_recipe_form=add_recipe_form)
