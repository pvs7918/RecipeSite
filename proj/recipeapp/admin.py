from datetime import timezone

from django.contrib import admin
from .models import Recipe, Category, Step, Ingredient



@admin.action(description="Сбросить количество в ноль")
def date_created_set_now(modeladmin, request, queryset):
    queryset.update(date_created=timezone.now)

class RecipeAdmin(admin.ModelAdmin):
    # список полей для отображения в списке Админ.панели
    list_display = ['name', 'time_cook', 'author', 'date_created']
    # поля только для чтения
    readonly_fields = []
    ordering = ['categories']  # Сортировка
    list_filter = ['categories', 'name', 'author']    # поля доступные для фильтрации (поиска)
    search_fields = ['description']        # текстовый поиск
    search_help_text = 'Полнотекстный поиск'  # описание к текстовому поиску
    actions = [date_created_set_now]

    # подробное отображение одной записи (с делением полей на абзацы)
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Подробности',
            {
                'description': 'Категории рецепта и подробное описание',
                'fields': ['categories', 'description', 'author', 'steps', 'ingredients'],
            },
        ),
        (
            'Прочее',
            {
                'description': 'Прочие детали',
                'fields': ['time_cook', 'date_created', 'foto'],
            }
        ),
    ]


admin.site.register(Category)
admin.site.register(Step)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
