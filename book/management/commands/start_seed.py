from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands import createsuperuser

from book.enums import PhoneTypes
from book.models import Employee, Organization, Phone


User = get_user_model()


class Command(createsuperuser.Command):
    help = 'Добавление тестовых данных'

    def handle(self, *args, **options):
        organization_1, is_create = Organization.objects.get_or_create(name='ООО Ромашка')
        organization_2, is_create = Organization.objects.get_or_create(name='ООО Василек')
        Organization.objects.get_or_create(name='ООО Гремучая ива')

        employee_1, is_create = Employee.objects.get_or_create(
            organization=organization_1, full_name='Иванов Сергей Петрович', post='Инженер'
        )
        employee_2, is_create = Employee.objects.get_or_create(
            organization=organization_1, full_name='Басурман Иван Павлович', post='Бухгалтер'
        )
        employee_3, is_create = Employee.objects.get_or_create(
            organization=organization_2, full_name='Цветкова Яна Ивановна', post='Программист'
        )

        Phone.objects.get_or_create(employee=employee_1, type=PhoneTypes.Fax, number='+74951234567')
        Phone.objects.get_or_create(employee=employee_2, type=PhoneTypes.Work, number='+79161234567')
        Phone.objects.get_or_create(employee=employee_2, type=PhoneTypes.Fax, number='+74951234567')
        Phone.objects.get_or_create(employee=employee_3, type=PhoneTypes.Personal, number='+79161234567')
        Phone.objects.get_or_create(employee=employee_3, type=PhoneTypes.Fax, number='+74951234567')

        self.stdout.write('Данные загружены.')
