from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email',
        'first_name', 'last_name',
        'bio', 'role')
    search_fields = ('username',)


admin.site.register(User, UserAdmin)
