# Маршруты
# Подключите маршруты, убедитесь в работоспособности представлений и связанных
# с ними моделей, форм и шаблонов.
from django.template.defaulttags import url
from django.urls import path
from .views import *

urlpatterns = [path('', index, name='recipeapp/index'),
               path('recipes/', recipes, name='recipeapp/recipes'),
               path('recipe/<int:recipe_id>/', recipe, name='recipeapp/recipe'),
               path('recipe_add/', recipe_add, name='recipeapp/recipe_add'),
               path('recipe_edit/<int:recipe_id>/', recipe_edit, name='recipeapp/recipe_edit'),
               path('recipe_del/<int:recipe_id>/', recipe_del, name='recipeapp/recipe_del'),

               # Категории
               path('categories/', categories, name='recipeapp/categories'),
               path('category/<int:category_id>/', category, name='recipeapp/category'),
               path('category_add/', category_add, name='recipeapp/category_add'),
               path('category_edit/<int:category_id>/', category_edit, name='recipeapp/category_edit'),
               path('category_del/<int:category_id>/', category_del, name='recipeapp/category_del'),

               path('about/', about, name='recipeapp/about'),
               path(r'^register/$', register, name='register'),
               ]
