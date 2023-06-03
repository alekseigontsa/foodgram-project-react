"""Модуль для заполнения базы данных из документов формата .csv.
Данные в документах должны быть структурированны согласно модели
 и в качестве разделителя используется запятая.
 Для загрузки данные должны находиться по пути ../data"""
import csv
from pathlib import Path

# from django.conf import settings
from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


def read_csv(file_name: str):
    # csv_path = Path(settings.BASE_DIR, '../data/', file_name)
    csv_path = Path('./data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    return csv.reader(csv_file, delimiter=',')


class Command(BaseCommand):
    """Парсер базы данных из файлов CSV."""
    help = 'load_csv'

    def handle(self, *args, **options):
        csv_reader = read_csv('ingredients.csv')
        next(csv_reader, None)
        for row in csv_reader:
            obj, created = Ingredient.objects.get_or_create(
                name=row[0],
                measurement_unit=row[1]
            )
        print('Ингредиенты - OK')
