from tokenize import Token
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import *


class UserAccountAdmin(admin.ModelAdmin):

    search_fields = ['email']
    class Meta:
        model = UserAccount

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    # fieldsets = (
    #     (None, {'fields': ('email', 'password','verified')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
    #                                    'groups', 'user_permissions')}),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2'),
    #     }),
    # )
    list_display = ('email', 'is_staff', 'verified')
    search_fields = ['email']
    ordering = ('email',)



admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(TokenList)