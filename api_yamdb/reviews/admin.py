from django.contrib import admin

from reviews.models import Title, Review


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description')
    search_fields = ('name', 'year',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'title',
        'text', 'score', 'created',
    )
    search_fields = ('author', 'title',)
    list_filter = ('author', 'title',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
