import csv
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Load csv data'

    def handle(self, *args, **kwargs):
        print('Reading User')
        with open('static/data/users.csv', encoding='utf-8') as user_csv:
            user_reader = csv.reader(user_csv)
            print(', '.join(str(p) for p in next(user_reader)))
            for row in user_reader:
                print(', '.join(str(p) for p in row))
                User(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                ).save()
            print('User done')

        print('Reading  Category')
        with open('static/data/category.csv', encoding='utf-8') as categ_csv:
            category_reader = csv.reader(categ_csv)
            print(', '.join(str(p) for p in next(category_reader)))
            for row in category_reader:
                print(', '.join(str(p) for p in row))
                Category(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                ).save()
            print('Catgory done')

        print('Reading Genre')
        with open('static/data/genre.csv', encoding='utf-8') as genre_csv:
            genre_reader = csv.reader(genre_csv)
            print(', '.join(str(p) for p in next(genre_reader)))
            for row in genre_reader:
                print(', '.join(str(p) for p in row))
                Genre(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                ).save()
            print('Genre done')

        print('Reading Title')
        with open('static/data/titles.csv', encoding='utf-8') as title_csv:
            title_reader = csv.reader(title_csv)
            print(', '.join(str(p) for p in next(title_reader)))
            for row in title_reader:
                print(', '.join(str(p) for p in row))
                category = Category.objects.get(id=row[3])
                Title(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=category
                ).save()
            print('Title done')

        print('Reading GenreTitle')
        with open('static/data/genre_title.csv', encoding='utf-8') as gt_csv:
            gt_reader = csv.reader(gt_csv)
            print(', '.join(str(p) for p in next(gt_reader)))
            for row in gt_reader:
                print(', '.join(str(p) for p in row))
                title_id = Title.objects.get(id=row[1])
                genre_id = Genre.objects.get(id=row[2])
                GenreTitle(
                    id=row[0],
                    title=title_id,
                    genre=genre_id
                ).save()
            print('GenreTitle done')

        print('Reading Review')
        with open('static/data/review.csv', encoding='utf-8') as review_csv:
            review_reader = csv.reader(review_csv)
            print(', '.join(str(p) for p in next(review_reader)))
            for row in review_reader:
                print(', '.join(str(p) for p in row))
                title = Title.objects.get(id=row[1])
                author = User.objects.get(id=row[3])
                Review(
                    id=row[0],
                    title_id=title.id,
                    text=row[2],
                    author=author,
                    score=row[4],
                    pub_date=row[5],
                ).save()
            print('Review done')

        print('Reading Comment')
        with open('static/data/comments.csv', encoding='utf-8') as comment_csv:
            comment_reader = csv.reader(comment_csv)
            print(', '.join(str(p) for p in next(comment_reader)))
            for row in comment_reader:
                print(', '.join(str(p) for p in row))
                review_id = Review.objects.get(id=row[1])
                author = User.objects.get(id=row[3])
                Comment.objects.create(
                    id=row[0],
                    review=review_id,
                    text=row[2],
                    author=author,
                    pub_date=row[4]
                ).save()
            print('Comment done')
