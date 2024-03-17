import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import NewUser

CSVFILES_DIRS = os.path.join(settings.BASE_DIR, r'static\data')
csvfiles_set = {
    'users': CSVFILES_DIRS + r'\users.csv',
    'category': CSVFILES_DIRS + r'\category.csv',
    'titles': CSVFILES_DIRS + r'\titles.csv',
    'genre': CSVFILES_DIRS + r'\genre.csv',
    'review': CSVFILES_DIRS + r'\review.csv',
    'comments': CSVFILES_DIRS + r'\comments.csv',
    'genre_title': CSVFILES_DIRS + r'\genre_title.csv',
}
tst = CSVFILES_DIRS + r'\category.csv'


def create_users(value):
    for row in value:
        user_instance = NewUser(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name'],
        )
        user_instance.save()


def create_category(value):
    for row in value:
        category_instance = Category(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        category_instance.save()


def create_titles(value):
    for row in value:
        title_instance = Title(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category_id=row['category']
        )
        title_instance.save()


def create_genre(value):
    for row in value:
        genre_instance = Genre(id=row['id'],
                               name=row['name'],
                               slug=row['slug'])
        genre_instance.save()


def create_review(value):
    for row in value:
        review_instance = Review(id=row['id'],
                                 title_id=row['title_id'],
                                 author_id=row['author'],
                                 score=row['score'],
                                 pub_date=row['pub_date'])
        review_instance.save()


def create_comments(value):
    for row in value:
        comment_instance = Comment(id=row['id'],
                                   review_id=row['review_id'],
                                   text=row['text'],
                                   author_id=row['author'],
                                   pub_date=row['pub_date'])
        comment_instance.save()


def create_genre_titles(value):
    for row in value:
        title_instance = Title.objects.get(id=row['title_id'])
        title_instance.genre.add(row['genre_id'])


class Command(BaseCommand):
    help = 'команда для импорта тестовых данных в базу Reviews из .csv фикстур'

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.WARNING('Запущен импорт данных в базу...')
        )

        func_set = [create_users,
                    create_category,
                    create_titles,
                    create_genre,
                    create_review,
                    create_comments,
                    create_genre_titles]
        try:
            for value, func_instance in zip(csvfiles_set.values(), func_set):
                with open(value, mode='r', encoding='utf-8') as csv_file:
                    dict_reader = csv.DictReader(csv_file)
                    func_instance(dict_reader)
            self.stdout.write(self.style.SUCCESS(
                'Данные успешно импортированы.')
            )
        except Exception:
            self.stderr.write(
                self.style.ERROR('Ошибка: данные не импортированы!')
            )
