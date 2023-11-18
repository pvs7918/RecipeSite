from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from recipeapp.models import Recipe, Category, Step, Ingredient
from django.contrib.auth.models import User

import os
import os.path
import json
import shutil
from django.conf import settings

#json-строка пустой БД. для случая когда изначально БД нет, либо файл БД утерян
empty_json_str = """
{
    "note": []
}
"""

def json_load_from_file(f_name):
    #если json-файл отсутствует, то предлагает создать пустой, по шаблону
    if not os.path.exists(f_name):
        print(f"Файл {f_name} не найден.")
        return False, []
    try:
        with open(f_name, "r", encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        return False, f'Ошибка чтения из файла {f_name}. {e}'
    return True, data


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        days_before = 500  # сколько дней назад от текущей даты для случайной генерации (нужно для фильтрации по дате добалвения товара, 7, 30, 365 дней)

        # предварительно запускаем команду очистки БД
        # предварительно очитаем таблицу в БД
        Category.objects.all().delete()
        Step.objects.all().delete()
        Ingredient.objects.all().delete()
        Recipe.objects.all().delete()

        #каталог с исходными файлами данных в формате json
        src_folder = os.path.abspath('recipeapp/management/commands/data/')

        # Добавление пользователей в БД, если их там нет
        f_name = os.path.join(src_folder, "users.json")
        status, list_dicts = json_load_from_file(f_name)  # считываем данные в список словарей
        users = []  # список объектов
        if status:
            for dict in list_dicts:
                # если пользователь не найден в БД
                if not User.objects.filter(username=dict["username"]).first():
                    # тогда создаем и добавляем его в БД
                    user = User.objects.create_user(username=dict["username"],
                                                    email=dict["email"],
                                                    password=dict["password"])
                    user.save()
                    users.append(user)
            print(f"Добавлено {len(users)} пользователей.\n")

        # Считываем Категории
        f_name = os.path.join(src_folder, "categories.json")
        print(f"{f_name=}")
        status, list_dicts = json_load_from_file(f_name) #считываем данные в список словарей
        categories = []    # список объектов
        if status:
            for dict in list_dicts:
                category = Category(pk=dict["pk"],
                                    name=dict["name"]
                                    )
                # category.save()  # v1 - каждый объект сохраняется отдельно в БД
                print(category)
                categories.append(category)  # в список добавляем id (pk) продукта
            Category.objects.bulk_create(categories)    # v2 групповое добавление объектов в БД
            print(f"Добавлено {len(categories)} категорий.\n")

        # Считываем Рецепты
        f_name = os.path.join(src_folder, "recipes.json")
        status, list_dicts = json_load_from_file(f_name)  # считываем данные в список словарей
        recipes = []    # список объектов
        # print(list_dicts)
        if status:
            # создаем объект - Рецепт и сохраняем в БД
            for dict in list_dicts:
                recipe = Recipe.objects.create(pk=dict["pk"],
                                name=dict["name"],
                                description=dict["description"],
                                time_cook=dict["time_cook"],
                                author=get_object_or_404(User, username=dict["author"]),
                                date_created=dict["date_created"],
                                foto=dict["foto"]
                                )
                recipe.categories.set(Category.objects.filter(name__in=dict["categories"]))
                recipe.save()  # v1 - каждый объект сохраняется отдельно в БД

                # фото копируем из подкаталога commands/data/images в каталог,
                # заданный в переменной MEDIA_ROOT в файле settings.py проекта
                images_folder = os.path.join(src_folder, "images")
                src_file = os.path.join(images_folder, dict["foto"])

                # копирование с перезаписью существующих файлов
                shutil.copy(src_file, settings.MEDIA_ROOT)

                # fs = FileSystemStorage()
                #fs.save(recipe.foto.name, recipe.foto)

                print(f"{src_file=} {recipe.foto.name=}, {recipe.foto=}")
                recipes.append(recipe)  # в список добавляем id (pk) продукта
            # Recipe.objects.bulk_create(recipes)    # v2 групповое добавление объектов в БД
            print(f"Добавлено {len(recipes)} рецепт(ов).\n")

        # Считываем Step - Шаги приготовления рецептов
        f_name = os.path.join(src_folder, "steps.json")
        status, list_dicts = json_load_from_file(f_name)  # считываем данные в список словарей
        steps = []  # список объектов
        if status:
            for dict in list_dicts:
                step = Step(pos=dict["pos"],
                            desc=dict["desc"]
                            )
                step.save()  # v1 - каждый объект сохраняется отдельно в БД
                # print(step)
                steps.append(step)  # в список добавляем id (pk) продукта

                # Добавляем шаг к нужному рецепту
                recipe = get_object_or_404(Recipe, pk=dict["recipe"])   # v2 групповое добавление объектов в БД
                recipe.steps.add(step)
                recipe.save()
            print(f"Добавлено {len(steps)} шагов.\n")

        # Считываем Ingredient - ингредиенты рецептов
        f_name = os.path.join(src_folder, "ingredients.json")
        status, list_dicts = json_load_from_file(f_name)  # считываем данные в список словарей
        ingredients = []  # список объектов
        if status:
            for dict in list_dicts:
                ingredient = Ingredient(name=dict["name"])
                ingredient.save()  # v1 - каждый объект сохраняется отдельно в БД
                #print(ingredient)
                ingredients.append(ingredient)  # в список добавляем id (pk) продукта
                # Добавляем ингредиент к нужному рецепту
                recipe = get_object_or_404(Recipe, pk=dict["recipe"])
                recipe.ingredients.add(ingredient)
                recipe.save()
            print(f"Добавлено {len(ingredients)} ингредиентов.\n")



        print("Выполнено add_data_to_db.")
#
# запуск:
# python manage.py add_data_to_db
