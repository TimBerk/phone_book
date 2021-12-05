from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

from book.enums import PhoneTypes
from book.managers import ContentTypeManager, OrganizationManager
from book.validators import phone_validator


User = get_user_model()


class OrganizationPermission(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        verbose_name='Тип данных',
        blank=True,
        null=True,
    )
    object_id = models.IntegerField('Объект', blank=True, null=True)
    user = models.ForeignKey(
        User,
        related_name='book_permissions',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    objects = models.Manager()
    content_objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Право организации'
        verbose_name_plural = 'Права организаций'
        indexes = [
            models.Index(fields=['object_id'])
        ]
        unique_together = ['content_type', 'object_id', 'user']

    def get_obj(self):
        model = apps.get_model(
            app_label=self.content_type.app_label,
            model_name=self.content_type.model
        )
        return model.objects.get(pk=self.object_id)


class Organization(models.Model):
    name = models.CharField('Название', max_length=512, unique=True, db_index=True)
    description = models.TextField('Описание', blank=True, null=True)
    address = models.TextField('Адрес', blank=True, null=True)
    owner = models.ForeignKey(
        User,
        related_name='organizations',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    objects = models.Manager()
    full_objects = OrganizationManager()

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Employee(models.Model):
    organization = models.ForeignKey(
        Organization,
        related_name='employees',
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )
    full_name = models.CharField('Название', max_length=512, db_index=True)
    post = models.CharField('Должность', max_length=512)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name

    def full_name_with_post(self):
        return f'{self.full_name} ({self.post})'


class Phone(models.Model):
    employee = models.ForeignKey(
        Employee,
        related_name='phones',
        on_delete=models.CASCADE,
        verbose_name='Сотрудник'
    )
    type = models.SmallIntegerField('Тип', choices=PhoneTypes.CHOICES, default=PhoneTypes.Personal)
    number = models.CharField(
        'Номер',
        max_length=50,
        db_index=True,
        validators=[phone_validator]
    )

    class Meta:
        verbose_name = 'Номер телефона'
        verbose_name_plural = 'Номера телефонов'

    def __str__(self):
        return self.number

    def number_with_type(self):
        type_name = ''
        for value, name in PhoneTypes.CHOICES:
            if value == self.type:
                type_name = name
        return f'{type_name}: {self.number}'
