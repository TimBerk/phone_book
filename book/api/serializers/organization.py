from rest_framework import serializers

from book.enums import PhoneTypes
from book.models import Employee, Organization, Phone


class PhoneListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='number_with_type', read_only=True)

    class Meta:
        model = Phone
        fields = ('id', 'name')


class PhoneSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='get_type_display')

    class Meta:
        model = Phone
        exclude = ('employee',)

    def validate(self, attrs):
        type_phone = attrs.get('type')
        if type_phone == PhoneTypes.Personal:
            query = Phone.objects.filter(number=attrs.get('number'), type=PhoneTypes.Personal)

            if self.instance:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise serializers.ValidationError({'number': 'Данный номер уже используется'})

        return attrs


class EmployeeListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name_with_post', read_only=True)
    phones = PhoneListSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'phones')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ('organization',)


class ListOrganizationSerializer(serializers.ModelSerializer):
    employees = EmployeeListSerializer(many=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'employees')


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ('owner',)
