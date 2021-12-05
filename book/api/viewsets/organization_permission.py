from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from book.api.serializers import (
    OrganizationPermissionListSerializer,
    OrganizationPermissionSerializer,
)
from book.helpers.decorators import lcd_schema_decorator
from book.helpers.mixins import ListCreateDestroyMixin, SelectSerializerMixin
from book.models import OrganizationPermission
from book.permissions import IsOwner


@lcd_schema_decorator(tags=['Права для организаций'])
class OrganizationPermissionViewSet(SelectSerializerMixin, ListCreateDestroyMixin):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = OrganizationPermission.content_objects.order_by('content_type', 'object_id').all()

    list_serializer_class = OrganizationPermissionListSerializer
    serializer_class = OrganizationPermissionSerializer
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return OrganizationPermission.objects.all()

            organization_ids = list(user.organizations.values_list('id', flat=True))
            return OrganizationPermission.content_objects.filter(
                content_type__model='organization',
                object_id__in=organization_ids
            ).all()
