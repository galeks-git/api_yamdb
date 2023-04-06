from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Title, Review, Genre, Category
from api.serializers import (
    TitleChangeSerializer, ReviewSerializer, CommentSerializer,
    CategorySerializer, GenreSerializer, TitleGETSerializer
)

from rest_framework.permissions import (
    # IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from api.permissions import (IsAuthorAdminModeratorOrReadOnly,
                             IsAdminOrReadOnly,
                             )
# from api.permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from api.pagination import PostsPagination
from .helper import CategoryANDGenreViewSet


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
    # permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    )
    # permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def get_title(self):
        return get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    )
    # permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    # def get_title(self):
    #     return get_object_or_404(
    #         Title, pk=self.kwargs.get('title_id')
    #     )

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments
        # return self.get_title().get_review().comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            # title=self.get_title(),
            review=self.get_review(),
        )
