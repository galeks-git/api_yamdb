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
 
    rating = serializers.SerializerMethodField()
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

    def get_rating(self, obj):
        rat = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        if rat is not None:
            return round(rat)
        else:
            return None


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate_score(self, value):
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
