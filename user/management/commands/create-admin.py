from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.db import IntegrityError


User = get_user_model()


class Command(createsuperuser.Command):
    help = 'Создание администратора'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Пароль',
        )

    def handle(self, *args, **options):
        password = options.get('password')
        email = options.get('email')

        if not password or not email:
            raise CommandError('--email и --password обязательные поля')

        try:
            user = User(
                email=email,
                is_staff=True,
                is_superuser=True
            )
            user.set_password(password)
            user.save()
            self.stdout.write('Пользователь создан успешно.')
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
