from django.contrib import admin
from accounts.models import User
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'name', ]


admin.site.register(User, UserAdmin)
