from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Title, Review, Comment, Genre, Category
from users.models import User


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
    genre = GenreSerializer(many=True)
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

    genre = serializers.SlugRelatedField(slug_field='slug',queryset=Genre.objects.all())

    category = serializers.SlugRelatedField(slug_field='slug',queryset=Category.objects.all()) 

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate_score(self, value):
        # if value < 1 or value > 10:
        if not (0 < value < 11):
            raise serializers.ValidationError('Score must between 1 and 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('title', 'review',)
