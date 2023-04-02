from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Title, Review, Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        # fields = '__all__'
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )

    def get_rating(self, obj):
        rat = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        return round(rat)

    def __str__(self):
        return self.name


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
