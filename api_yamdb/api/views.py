from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ValidationError
from rest_framework import viewsets
# from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (
    # IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    # AllowAny,
)

from reviews.models import Title, Review, Genre, Category
from api.pagination import PostsPagination
from api.helper import CategoryANDGenreViewSet
from api.permissions import (
    # IsAuthorOrReadOnly,
    IsAdminOrReadOnly,
    IsAuthorAdminModeratorOrReadOnly,
)
from api.serializers import (
    TitleChangeSerializer, ReviewSerializer, CommentSerializer,
    CategorySerializer, GenreSerializer, TitleGETSerializer
)


class CategoryViewSet(CategoryANDGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryANDGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg("reviews__score")).order_by("name")
    serializer_class = TitleChangeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleChangeSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    )
    pagination_class = PostsPagination

    def get_title(self):
        return get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        queryset = Review.objects.filter(title=self.get_title())
        return queryset
        # return self.get_title().reviews.all()

    def perform_create(self, serializer):
        if not Review.objects.filter(author=self.request.user).exists():
            return serializer.save(
                author=self.request.user,
                title=self.get_title()
            )
        else:
            raise ValidationError('You can make review only one time')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    )
    pagination_class = PostsPagination

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()
        # return self.get_title().get_review().comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            # title=self.get_title(),
            review=self.get_review(),
        )
