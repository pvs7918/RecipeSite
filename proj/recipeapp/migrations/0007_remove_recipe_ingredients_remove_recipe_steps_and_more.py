# Generated by Django 4.2.7 on 2023-11-16 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0006_ingredient_step_alter_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='steps',
        ),
        migrations.RemoveField(
            model_name='step',
            name='name',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recept',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='recipeapp.recipe'),
        ),
        migrations.AddField(
            model_name='step',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='step',
            name='recept',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='recipeapp.recipe'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=300),
        ),
    ]