from django.contrib import admin

from api.models import Categories
from api.models import Genres
from api.models import Titles


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'category_description',)
    search_fields = ('name', 'slug',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'genre_description', )
    search_fields = ('name', 'slug',)
    empty_value_display = '-пусто-'


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        # 'genre',
        'category',
    )
    search_fields = ('name', 'year', 'category')
    list_filter = ('year', 'category')
    empty_value_display = '-пусто-'


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Titles, TitlesAdmin)
