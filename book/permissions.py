from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from book.models import Employee, Organization, OrganizationPermission, Phone


class IsOwner(IsAuthenticated):
    """
    Позволяет только администраторам и владельцам редактировать контент
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif not request.user.is_authenticated:
            return False

        organization_id = None
        is_organization = isinstance(obj, Organization)
        is_permission = isinstance(obj, OrganizationPermission)

        if is_organization:
            organization_id = obj.id
        elif isinstance(obj, Employee):
            organization_id = obj.organization_id
        elif isinstance(obj, Phone):
            organization_id = obj.employee.organization_id
        elif is_permission:
            organization_id = obj.object_id

        is_admin = request.user.is_superuser
        is_owner = request.user.organizations.filter(pk=organization_id).exists()
        is_manager = (not is_organization
                      and not is_permission
                      and OrganizationPermission.objects.filter(
                          content_type__model='organization',
                          object_id=organization_id,
                          user=request.user
                      ).exists())

        return is_admin or is_owner or is_manager


class IsOwnerOrReadOnly(IsOwner):
    """
    Позволяет всем пользователям просматривать контент,
    но редактировать его могут администраторы и владельцы,
    авторизованные пользователи могут редактировать только свои записи
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated
