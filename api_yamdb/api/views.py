from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (
    # IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from reviews.models import Title, Review, Genre, Category
from api.pagination import PostsPagination
from api.permissions import (
    IsAuthorOrReadOnly, IsAdminOrReadOnly,
    IsAuthorAdminModeratorOrReadOnly,
)
from api.serializers import (
    TitleSerializer, ReviewSerializer, CommentSerializer,
    CategorySerializer, GenreSerializer
)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (IsAdmin,)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (AllowAny,)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = PostsPagination
    # permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


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
