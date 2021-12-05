from rest_framework import routers

from book.api.viewsets import (
    EmployeeViewSet,
    OrganizationPermissionViewSet,
    OrganizationViewSet,
    PhoneViewSet,
)


router = routers.DefaultRouter()

router.register(
    r'organizations/permissions',
    OrganizationPermissionViewSet,
    basename='organizations-permissions'
)
router.register(
    'organizations',
    OrganizationViewSet,
    basename='organizations'
)
router.register(
    r'organizations/(?P<org_id>\d+)/employees',
    EmployeeViewSet,
    basename='employees'
)
router.register(
    r'organizations/(?P<org_id>\d+)/employees/(?P<emp_id>\d+)/phones',
    PhoneViewSet,
    basename='phones'
)
