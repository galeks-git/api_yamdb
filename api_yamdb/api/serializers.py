from datetime import datetime
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.serializers import IntegerField

from reviews.models import Title, Review, Comment, Genre, Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGETSerializer(serializers.ModelSerializer):
    """ Сериализатор для GET запросов"""
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

class TitleChangeSerializer(serializers.ModelSerializer):
    """Сериализатор при небезопасных запросах."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    year = IntegerField()

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = datetime.now().year
        if value > year:
            raise serializers.ValidationError(
                f'Year не может быть больше {year}')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('title', 'review',)
