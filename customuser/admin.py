from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, User_Account, Countries, DateFormat


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_superuser',)
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'email')  # 🖘 no username
    fieldsets = (
        (
            'Fields',
            {
                'fields': (
                    'email',
                    'password',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'last_login',
                    'date_joined',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(User_Account)
admin.site.register(Countries)
admin.site.register(DateFormat)

