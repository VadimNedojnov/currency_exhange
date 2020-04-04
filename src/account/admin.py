from django.contrib import admin


from account.models import User


class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'username', 'is_active', 'avatar']


admin.site.register(User, UserAdmin)
