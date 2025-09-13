from django.contrib.auth import authenticate
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from notebook.models import ErrorMessage


class Command(BaseCommand):
    """
    Пользовательская команда заполнения таблицы базы данных с сообщениями об ошибках
    Как пользоваться:
    находясь в каталоге приложения, ввести в командной строке python manage.py create_error_messages
    """
    help = "Пользовательская команда заполнения таблицы базы данных с сообщениями об ошибках"

    def handle(self, *args, **kwargs) -> None:
        messages = [(1, 'Неизвестная ошибка'),
                    (100, 'Не удалось создать блокнот по неуказанной причине'),
                    (101, 'Блокнот с таким названием уже существует'),
                    ]

        ErrorMessage.objects.all().delete()

        for data in messages:
            error_message = ErrorMessage.objects.create(id=data[0], name=data[1])
                # mailing_id = int(input('Введите id рассылки: '))
                # mailing = get_object_or_404(Mailing, pk=mailing_id)
                # mailing.send()
                # attempts = Attempt.objects.filter(mailing=mailing_id).order_by('-date_time')
                # if attempts:
                #     message = f"попытка рассылки сообщения '{mailing.message.topic}' {attempts[0].date_time}"
                #     if attempts[0].is_successful:
                #         message += ' прошла успешно'
                #     else:
                #         message += 'не удалась'
                #     # print(message)
