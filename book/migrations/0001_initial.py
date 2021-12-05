# Generated by Django 3.2.9 on 2021-12-05 13:53

import book.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(db_index=True, max_length=512, verbose_name='Название')),
                ('post', models.CharField(max_length=512, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(1, 'Рабочий'), (2, 'Личный'), (3, 'Факс')], default=2, verbose_name='Тип')),
                ('number', models.CharField(db_index=True, max_length=50, validators=[book.validators.phone_validator], verbose_name='Номер')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='book.employee', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Номер телефона',
                'verbose_name_plural': 'Номера телефонов',
            },
        ),
        migrations.CreateModel(
            name='OrganizationPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(blank=True, null=True, verbose_name='Объект')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype', verbose_name='Тип данных')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_permissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Право организации',
                'verbose_name_plural': 'Права организаций',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=512, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Адрес')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='book.organization', verbose_name='Организация'),
        ),
        migrations.AddIndex(
            model_name='organizationpermission',
            index=models.Index(fields=['object_id'], name='book_organi_object__f77b22_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='organizationpermission',
            unique_together={('content_type', 'object_id', 'user')},
        ),
    ]
