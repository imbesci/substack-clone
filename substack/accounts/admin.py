from django.contrib import admin
from .models import SubstackUser
from django.contrib.auth.admin import UserAdmin

class SubstackAdmin(UserAdmin):
    list_display = ( 'email', 'username', 'first_name', 
                    'date_joined', 'password', 'last_login', 
                    'is_admin','is_staff' )
    search_fields = ( 'email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('General', {
            'fields' : ('first_name', 'last_name', 'email',
                'username', 'password', 'date_joined', 'last_login')
        }),

        ('Advanced options', {
            'classes': ('collapse', ),
            'fields' : ('is_admin', 'is_staff', 'is_superuser'),
            }),
        )   

admin.site.register(SubstackUser, SubstackAdmin)
