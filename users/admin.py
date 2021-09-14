from django.contrib import admin
from .models import NewUser
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'username', 'firstname',)
    list_filter = ('email', 'username', 'firstname', 'is_active', 'is_staff','id')
    ordering = ('-date_joined',)
    list_display = ('email', 'username', 'firstname',
                    'is_active', 'is_staff', 'id')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'firstname', 'id')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about', 'phone', 'college', 'department', 'degree', 'course_duration' ,'graduation_year', 'provider')}),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'firstname', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Profile)
