from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Title, Review
from api.serializers import (
    TitleSerializer, ReviewSerializer, CommentSerializer
)

# from rest_framework import filters
# from rest_framework import mixins
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from api.permissions import IsAuthorOrReadOnly
# from api.permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from api.pagination import PostsPagination


# class GroupViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


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
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
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
