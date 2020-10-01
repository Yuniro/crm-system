from django.contrib import admin

# Register your models here.

from crm.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Employer


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'domains', 'logo')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'permission')


class EmployerUser(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Employer
    list_display = ('username', 'is_staff', 'is_active', 'is_owner', 'first_name', 'last_name', 'company', 'language', 'passport', 'phone_number',
                    'department', 'permission')
    list_filter = ('username', 'is_staff', 'is_active', 'first_name', 'last_name', 'is_owner', 'company', 'language', 'passport', 'phone_number',
                   'department', 'permission')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'company', 'language', 'passport',
                           'phone_number', 'department', 'permission')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_owner')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_owner')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(Employer, EmployerUser)
