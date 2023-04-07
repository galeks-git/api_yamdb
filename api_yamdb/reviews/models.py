from django.db.models import UniqueConstraint
from django.db import models

from users.models import User


class Category(models.Model):
    """Модель Категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название Категории'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug',
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанров."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Slug',
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=256)
    year = models.IntegerField(verbose_name='Год написания')
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["title", "author", ],
                name='unique_review',
            ),
        ]


class Comment(models.Model):
    """Модель комментарии к отзывам."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class GenreTitle(models.Model):

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        verbose_name_plural = 'Таблица соответствия жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру {self.genre} '
