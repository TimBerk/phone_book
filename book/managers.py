from django.db import models


class OrganizationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('employees', 'employees__phones')


class ContentTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('content_type', 'user')
