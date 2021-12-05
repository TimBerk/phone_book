from phone_book.celery_settings import app

from book.models import Employee


@app.task
def remove_employees_without_phones():
    """Удаление сотрудников без контактов"""
    Employee.objects.filter(phones__isnull=True).all().delete()
