from django.contrib import admin
from .models import NewUser
from .models import UserSingle
from .models import UserGroup
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'username', 'firstname',)
    list_filter = ('email', 'username', 'firstname',
                   'is_active', 'is_staff', 'id','points','tasks')
    ordering = ('-date_joined',)
    list_display = ('email', 'username', 'firstname',
                    'is_active', 'is_staff', 'id', 'alcherid')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'firstname', 'id', 'alcherid','points')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('img', 'about', 'phone', 'college_state', 'graduation_year', 'college_city',
         'college_name', 'position_of_responsibility', 'interested_modules', 'referred_by', 'referrals', 'provider')}),
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
admin.site.register(UserSingle)
admin.site.register(UserGroup)
