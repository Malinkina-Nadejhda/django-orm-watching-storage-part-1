import os
import argparse
import random

import django
from django.db.utils import OperationalError
from django.core.exceptions import ImproperlyConfigured

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from datacenter.models import Passcard  # noqa: E402


def main():
    parser = argparse.ArgumentParser(
        description=r"""
        Скрипт для работы с базой данных пропусков.
        Пример ввода:
        python .\test2.py --mode count # Общее количество пропусков.
        python .\test2.py --mode active # Количество активных пропусков.
        python .\test2.py --mode info # Информация из случайного пропуска.
        """,
        epilog="""
        Для работы программы требуется файл .env с настройками базы данных.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter

    )

    parser.add_argument(
        "--mode",
        choices=["count", "active", "info"],
        default="count",
        help="""
        Режимы работы программы: 
        count - общее количество пропусков, 
        active - количество активных пропусков, 
        info - информация из случайного пропуска,
        default - all
        """
    )
    args = parser.parse_args()
    try:
        passcards = Passcard.objects.all()
        total_passcards = Passcard.objects.count()

        if args.mode == "count":
            print('Всего пропусков:', total_passcards)
        elif args.mode == "active":
            active_passcards = Passcard.objects.filter(is_active=True)
            print(f'Активных пропусков: {active_passcards.count()}')
        elif args.mode == "info":
            some_index = random.randint(0, len(passcards) - 1)
            some_passcard = passcards[some_index]
            print(
                f"owner_name: {some_passcard.owner_name}\n"
                f"passcode: {some_passcard.passcode}\n"
                f"created_at: {some_passcard.created_at}\n"
                f"is_active: {some_passcard.is_active}"
            )
    except OperationalError:
        print(
            "Ошибка подключения к базе данных.\n"
            "Проверьте настройки подключения в файле .env\n"
        )
    except ImproperlyConfigured:
        print(
            "Ошибка конфигурации.\n"
            "Проверьте заполнены ли все обязательные поля!"
        )


if __name__ == '__main__':
    main()