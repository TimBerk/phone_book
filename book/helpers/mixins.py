from rest_framework import mixins, viewsets


class SelectSerializerMixin(object):
    serializer_class = None
    list_serializer_class = None
    retrieve_serializer_class = None
    update_serializer_class = None
    partial_update_serializer_class = None
    create_serializer_class = None

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        """
        assert self.serializer_class is not None, (
            '"%s" should either include a `serializer_class` attribute, '
            'or override the `get_serializer_class()` method.' % self.__class__.__name__
        )
        return getattr(self, f'{self.action}_serializer_class') or self.serializer_class


class ListCreateDestroyMixin(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """
    Миксин для списка, создания и удаления объектов.
    """
