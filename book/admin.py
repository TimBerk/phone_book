from nested_admin.nested import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedTabularInline,
)

from django.contrib import admin

from book.models import Employee, Organization, OrganizationPermission, Phone


class PhoneInlineAdmin(NestedTabularInline):
    raw_id_fields = ('employee',)
    model = Phone
    extra = 0


class EmployeeInlineAdmin(NestedStackedInline):
    inlines = [PhoneInlineAdmin]
    raw_id_fields = ('organization',)
    model = Employee
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(NestedModelAdmin):
    inlines = [EmployeeInlineAdmin]
    search_fields = ('name',)


@admin.register(OrganizationPermission)
class OrganizationPermissionAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user',)
