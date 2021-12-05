from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Q

from book.api.serializers import (
    EmployeeListSerializer,
    EmployeeSerializer,
    ListOrganizationSerializer,
    OrganizationSerializer,
    PhoneListSerializer,
    PhoneSerializer,
)
from book.helpers.decorators import common_schema_decorator
from book.helpers.mixins import SelectSerializerMixin
from book.models import Employee, Organization, OrganizationPermission, Phone
from book.permissions import IsOwnerOrReadOnly


@common_schema_decorator(tags=['Организации'])
class OrganizationViewSet(SelectSerializerMixin, viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Organization.full_objects.order_by('id').all()
    filter_backends = (SearchFilter,)
    search_fields = ['name', 'employees__full_name', 'employees__phones__number']
    serializer_class = OrganizationSerializer
    list_serializer_class = ListOrganizationSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        operation_summary='Список организаций пользователя',
        tags=['Организации']
    )
    @action(
        methods=['GET'],
        url_path="my",
        detail=False,
        serializer_class=ListOrganizationSerializer,
        permission_classes=[IsAuthenticated]
    )
    def get_my_organizations(self, request, *args, **kwargs):
        manage_organizations = list(OrganizationPermission.objects.filter(
            content_type__model='organization', user=request.user
        ).values_list('object_id', flat=True))
        queryset = self.queryset.filter(Q(owner_id=request.user) | Q(pk__in=manage_organizations))
        serializer = ListOrganizationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@common_schema_decorator(tags=['Сотрудники'])
class EmployeeViewSet(SelectSerializerMixin, viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EmployeeSerializer
    list_serializer_class = EmployeeListSerializer

    def get_queryset(self):
        organization = get_object_or_404(
            Organization.full_objects,
            pk=self.kwargs.get('org_id')
        )
        return organization.employees.all()

    def perform_create(self, serializer):
        org_id = self.kwargs.get('org_id')
        get_object_or_404(Organization, pk=org_id)
        serializer.save(organization_id=org_id)


@common_schema_decorator(tags=['Телефоны'])
class PhoneViewSet(SelectSerializerMixin, viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PhoneSerializer
    list_serializer_class = PhoneListSerializer

    def get_queryset(self):
        employee = get_object_or_404(
            Employee,
            organization_id=self.kwargs.get('org_id'),
            pk=self.kwargs.get('emp_id')
        )
        return employee.phones.all()

    def perform_create(self, serializer):
        emp_id = self.kwargs.get('emp_id')
        get_object_or_404(Employee, pk=emp_id)
        serializer.save(employee_id=emp_id)

    def perform_destroy(self, instance):
        if Phone.objects.filter(employee=instance.employee).count() == 1:
            raise ValidationError('Нельзя удалить единственный контакт')
        instance.delete()
