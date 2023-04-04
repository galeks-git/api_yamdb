from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Title, Review, Comment, Genre, Category
from users.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


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
        if rat is not None:
            return round(rat)
        else:
            # raise serializers.Error('No reviews for calc rating')
            return 'No reviews for calc rating'

    def __str__(self):
        return self.name


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    # title = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=User.objects.all(),
    # )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate_score(self, value):
        # if value < 1 or value > 10:
        if not (0 < value < 11):
            raise serializers.ValidationError('Score must between 1 and 10')
        return value

    def validate_title(self, value):
        queryset = Review.objects.filter(title=value)
        if queryset:
            raise serializers.ValidationError('You can make review only one time')
        return value

    # def validate_author(self, value):
    #     if value == self.context['request'].user:
    #         raise serializers.ValidationError('You can not follow yourself')
    #     return value

# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all(),
#         default=serializers.CurrentUserDefault(),
#     )
#     following = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all(),
#     )

#     class Meta:
#         model = Follow
#         fields = '__all__'

#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following'),
#                 message="UniqueTogetherValidator check"
#             )
#         ]

#     def validate_following(self, value):
#         if value == self.context['request'].user:
#             raise serializers.ValidationError('You can not follow yourself')
#         return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('title', 'review',)
