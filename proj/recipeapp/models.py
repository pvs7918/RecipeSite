from datetime import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings

# Краткое описание задания
# Используя фреймворк Django создайте сайт, на котором пользователи смогут
# добавлять свои рецепты блюд и просматривать рецепты других пользователей.

# Подробное описание задания
# Создайте проект Django и приложение(я) для сайта рецептов.
# Модели
# Для работы с пользователями используйте встроенного в Django User`a.
# Подготовьте нижеперечисленные модели:
# ● Рецепты:
# ○ Название
# ○ Описание
# ○ Шаги приготовления
# ○ Время приготовления
# ○ Изображение
# ○ Автор
# ○ *другие поля на ваш выбор, например ингредиенты и т.п.

# ● *Категории рецептов
# ○ Название
# ○ *другие поля на ваш выбор

# ● *Связующая таблица для связи Рецептов и Категории
# ○ *обязательные для связи поля
# ○ *другие поля на ваш выбор

# используем встроенную модель пользователя для авторизации
from django.contrib.auth.models import User


# Пользователи сайта
# class User(models.Model):
#     name = models.ForeignKey(User, on_delete=models.CASCADE)

# Модель Категория рецептов
class Category(models.Model):
    name = models.CharField(default='', max_length=100, unique=True)

    def __str__(self):
        return self.name
        # return f'Категория id: {self.pk}, название: {self.name}'


# Шаги приготовления рецепта
class Step(models.Model):
    pos = models.IntegerField(default=1)
    desc = models.CharField(max_length=300, default='')

    def __str__(self):
        return f'{self.pos}. {self.desc}'
        # return f'Шаг приготовления id: {self.pk}, описание: {self.desc}'


# Ингредиенты для рецепта
class Ingredient(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
        # return f'Ингредиент id: {self.pk}, название: {self.name}'


# Рецепт
class Recipe(models.Model):
    name = models.CharField(max_length=100)  # Название
    description = models.TextField()  # Описание
    categories = models.ManyToManyField(Category)
    steps = models.ManyToManyField(Step)
    ingredients = models.ManyToManyField(Ingredient)
    time_cook = models.CharField(default='', max_length=50)  # Время приготовления
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь сайта, который разместил рецепт
    date_created = models.DateTimeField(default=timezone.now)  # дата создания рецепта на сайте
    foto = models.ImageField(upload_to='media', blank=True)  # фото блюда

    def get_categories(self):
        return ", ".join(self.categories.all())

        # res = ""
        # for i, category in enumerate(self.categories.all()):
        #     if i > 0:
        #         res += ", " + category
        #     else:
        #         res += category
        #
        # return res

        #     return ", ".join(categories_list)
        # else:
        #     return ""

    def get_ingredients(self):
        if len(self.ingredients) > 0:
            return ", ".join(self.ingredients)
        else:
            return ""

    def get_steps(self):
        if len(self.steps) > 0:
            return ", ".join(self.steps)
        else:
            return ""

    def __str__(self):
        return f'Рецепт {self.pk}: {self.name}'

    def __repr__(self):
        return f'Рецепт id: {self.pk}, название: {self.name}, описание={self.description}' \
               f'время приготовления: {self.time_for_cooking}, дата создания: {self.date_created}.'
