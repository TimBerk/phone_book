from functools import singledispatch
from typing import List

from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet

from django.utils.decorators import method_decorator


def common_schema_decorator(tags: List[str]):
    @singledispatch
    def wrapper(origin_class_type):
        return origin_class_type

    @wrapper.register(type(ViewSet))
    def _(origin_class_type):
        method_decorator(
            name='list',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Список'
            ),
        )(origin_class_type)
        method_decorator(
            name='create',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Создание'
            ),
        )(origin_class_type)
        method_decorator(
            name='retrieve',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Получение'
            ),
        )(origin_class_type)
        method_decorator(
            name='update',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Обновление'
            ),
        )(origin_class_type)
        method_decorator(
            name='partial_update',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Частичное обновление', auto_schema=None
            ),
        )(origin_class_type)
        method_decorator(
            name='destroy',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Удаление'
            ),
        )(origin_class_type)

        return origin_class_type

    return wrapper


def lcd_schema_decorator(tags: List[str]):
    @singledispatch
    def wrapper(origin_class_type):
        return origin_class_type

    @wrapper.register(type(ViewSet))
    def _(origin_class_type):
        method_decorator(
            name='list',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Список'
            ),
        )(origin_class_type)
        method_decorator(
            name='create',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Создание'
            ),
        )(origin_class_type)
        method_decorator(
            name='destroy',
            decorator=swagger_auto_schema(
                tags=tags, operation_summary='Удаление'
            ),
        )(origin_class_type)

        return origin_class_type

    return wrapper
