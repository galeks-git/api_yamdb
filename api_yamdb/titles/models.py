from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    # genre = models.ForeignKey(
    #     Genre, on_delete=models.SET_NULL,
    #     related_name='genre_posts', blank=True, null=True
    # )
    # category = models.ForeignKey(
    #     Category, on_delete=models.SET_NULL,
    #     related_name='category_posts', blank=True, null=True
    # )

    def __str__(self):
        return self.name


class Review(models.Model):
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


# class Group(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()

#     def __str__(self):
#         return self.title


# class Post(models.Model):
#     text = models.TextField()
#     pub_date = models.DateTimeField(
#         'Дата публикации', auto_now_add=True
#     )
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='posts'
#     )
#     image = models.ImageField(
#         upload_to='posts/', null=True, blank=True
#     )  # поле для картинки
#     group = models.ForeignKey(
#         Group, on_delete=models.SET_NULL,
#         related_name='posts', blank=True, null=True
#     )

#     def __str__(self):
#         return self.text


# class Comment(models.Model):
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='comments'
#     )
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='comments'
#     )
#     text = models.TextField()
#     created = models.DateTimeField(
#         'Дата добавления', auto_now_add=True, db_index=True
#     )
