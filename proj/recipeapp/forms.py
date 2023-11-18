# Формы
# Создайте формы для ввода и редактирования информации (рецептов) в вашем
# проекте. Интегрируйте их в шаблоны.

import datetime
from datetime import timezone
from django.contrib.auth.models import User
from django import forms
from .models import Category
from django.contrib.auth.models import User


class CreateCategoryForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)  # Название

class EditCategoryForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)  # Название

    class Meta:
        model = Category

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        super().__init__(*args, **kwargs)

class CreateRecipeForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)  # Название
    description = forms.CharField(max_length=200)  # Описание
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    steps = forms.CharField(widget=forms.Textarea)  # шаги приготовления. Список с разделителем !
    time_for_cooking = forms.TimeField(required=True)  # Время приготовления
    foto = forms.ImageField()




class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']