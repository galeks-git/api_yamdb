from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Класс Категорий"""
    name = models.CharField(
                            max_length=256,
                            verbose_name='Название Категории'
                            )

    slug = models.SlugField(
                            max_length=75,
                            verbose_name='Slug',
                            unique=True
                            )
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанров"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug',
        unique=True)
    
    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений"""

    name = models.CharField(max_length=256)
    year = models.IntegerField(verbose_name='Год написания')
    description = models.TextField(blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,related_name='genre_posts', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,related_name='category_posts', blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.IntegerField()