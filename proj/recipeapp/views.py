import random

from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreateRecipeForm, CreateCategoryForm, EditCategoryForm, UserRegistrationForm
from .models import Recipe, Step, Ingredient, Category
from django.contrib.auth import login, authenticate

# Шаблоны
# Подготовьте базовый шаблон проекта и нижеперечисленные дочерние шаблоны:
# ● Главная с 5 случайными рецептами кратко
# ● Страница с одним подробным рецептом
# ● Страницы регистрации, авторизации и выхода пользователя
# ● Страница добавления/редактирования рецепта
# ● *другие шаблоны на ваш выбор


# Представления
# Создайте представления, которые охватывают весь ваш проект: модели, формы,
# шаблоны.


def index(request):
    # Отобразить 5 случайных рецептов
    # список всех pk всех рецептов
    recipes_ids = list(Recipe.objects.all().values_list('pk', flat=True))  # <--- [ First Query Hit ]
    # с помощью sample получаем случайную уникальную выборку из 5 элементов
    rnd_recipes_ids = random.sample(recipes_ids, 5)
    selected_recipes = Recipe.objects.filter(pk__in=rnd_recipes_ids)
    return render(request, 'recipeapp/recipes.html',
                  {'recipes': selected_recipes,
                   'my_title': "5 случайных рецептов"})



def about(request):
    return render(request, 'recipeapp/about.html')


def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipeapp/recipes.html',
                  {'recipes': recipes,
                   'my_title': "Все рецепты"})


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    categories = Category.objects.filter(recipe=recipe)
    steps = Step.objects.filter(recipe=recipe)
    ingredients = Ingredient.objects.filter(recipe=recipe)
    return render(request, 'recipeapp/recipe.html',
                  {'recipe': recipe})


def recipe_edit(request, recipe_id):
    return HttpResponse(f"Редактирование рецепта. {recipe_id}. Доработка")


def recipe_del(request, recipe_id):
    Recipe.objects.filter(pk=recipe_id).delete()
    return recipes(request)


def recipe_add(request):
    return HttpResponse(f"Добавление рецепта. Доработка")

    # if request.method == 'POST':
    #     form = CreateRecipeForm(request.POST, request.FILES)  # создаем форму с переданными данными
    #     if form.is_valid():
    #         # Если форма проходит валидацию(все поля заполнены корректно), то мы получаем данные
    #         # из формы и можем с ними работать.
    #         name = form.cleaned_data['name']
    #         description = form.cleaned_data['description']
    #         steps = form.cleaned_data['steps']
    #         time_for_cooking = form.cleaned_data['time_for_cooking']
    #         author_id = form.cleaned_data['author_id']
    #         date_created = form.cleaned_data['date_created']
    #         foto = form.cleaned_data['foto']
    #
    #         # сохраняем фото в спец каталог заданный в переменной MEDIA в файле settings.py проекта
    #         fs = FileSystemStorage()
    #         fs.save(foto.name, foto)
    #
    #         recipe = Recipe(name=name, description=description, steps=steps,
    #                         time_for_cooking=time_for_cooking, author_id=author_id,
    #                         date_created=date_created, foto=foto)
    #         recipe.save()
    #         message = 'Товар сохранён в БД.'
    #         # после добавления покаызваем все товары
    #         return recipes(request)  # вызываем метод возвращающий полный список рецептов
    # else:
    #     # Если запрос пришел методом GET, то мы просто создаем пустой экземпляр формы UserForm
    #     # и передаем его в шаблон user_form.html.
    #     form = CreateRecipeForm()
    #     # В шаблоне user_form.html мы можем вывести нашу форму с помощью тега {{form}}.
    #     message = 'Добавление товара'
    #     return render(request, 'recipeapp/recipe_add.html',
    #                   {'form': form, 'message': message})


def categories(request):
    categories = Category.objects.all()
    return render(request, 'recipeapp/categories.html',
                  {'categories': categories})


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'recipeapp/category.html',
                  {'category': category})


def category_add(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)  # создаем форму с переданными данными
        if form.is_valid():
            name = form.cleaned_data['name']
            category = Category(name=name)
            try:
                category.save()
                message = 'Категория сохранена в БД.'
                return categories(request)
            except IntegrityError as e:
                message = "Ошибка! Такая категория уже есть в БД. Введите другое название."
                form = CreateCategoryForm()
                return render(request, 'recipeapp/category_add.html',
                              {'form': form, 'message': message})
    else:
        message = 'Добавление категории'
        form = CreateCategoryForm()
        return render(request, 'recipeapp/category_add.html',
                      {'form': form, 'message': message})


def category_edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        form = EditCategoryForm(request.POST)
        if form.is_valid():
            # category = Category.objects.get(pk=category_id)
            category = get_object_or_404(Category, pk=category_id)
            category.name = form.cleaned_data['name']
            try:
                category.save()
                message = 'Категория обновлена в БД.'
                #возврат к полному списку категорий
                return categories(request)
            except IntegrityError as e:
                message = "Ошибка! Такая категория уже есть в БД. Введите другое название."
                form = EditCategoryForm(initial={'pk': category_id,
                                                 'name': category.name}, )
                return render(request, 'recipeapp/category_edit.html',
                              {'form': form, 'message': message})
    else:
        message = 'Редактирование категории'
        category = get_object_or_404(Category, pk=category_id)
        form = EditCategoryForm(initial={'pk': category_id,
                                     'name': category.name}, )
    return render(request, 'recipeapp/category_edit.html',
                  {'form': form, 'message': message})


def category_del(request, category_id):
    Category.objects.filter(pk=category_id).delete()
    return categories(request)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'recipeapp/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'recipeapp/register.html', {'user_form': user_form})
