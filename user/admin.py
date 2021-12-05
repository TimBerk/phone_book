from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')},
        ),
        (
            'Личная информация',
            {'fields': ('first_name', 'last_name',)},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
    list_display = ('id', 'email', 'is_staff')
    list_display_links = ('email',)
    list_filter = (
        'is_staff',
        'is_superuser',
        'groups'
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('pk',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
