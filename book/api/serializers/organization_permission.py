from crum import get_current_user
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from book.models import OrganizationPermission


User = get_user_model()


class OrganizationPermissionListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_object_name')
    user = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = OrganizationPermission
        fields = ('id', 'name', 'user')

    def get_object_name(self, obj):
        return obj.get_obj().name


class OrganizationPermissionSerializer(OrganizationPermissionListSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = OrganizationPermission
        fields = ('id', 'object_id', 'email')
        whire_only_fields = ('object_id',)

    def validate(self, attrs):
        object_id = attrs.get('object_id')
        email = attrs.get('email')
        user: User = get_current_user()

        if email == user.email:
            raise serializers.ValidationError({'email': 'Нельзя добавлять права самому себе'})

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Пользователя с данным email нет'})

        if not user.organizations.filter(pk=object_id).exists() and not user.is_superuser:
            raise serializers.ValidationError({'email': 'Вы не являетесь владельцем организации'})

        if OrganizationPermission.objects.filter(
                content_type__model='organization', user__email=email, object_id=object_id
        ).exists():
            raise serializers.ValidationError({'email': 'Права уже добавлены'})

        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email')
        validated_data['user'] = User.objects.filter(email=email).first()
        validated_data['content_type'] = ContentType.objects.filter(model='organization').first()
        return super().create(validated_data)
