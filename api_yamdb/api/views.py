from django.shortcuts import get_object_or_404
from api.permissions import IsAdmin
from rest_framework import viewsets, filters 
from rest_framework.permissions import AllowAny
from reviews.models import Title, Review, Genre, Category
from api.serializers import (
    TitleSerializer, ReviewSerializer, CommentSerializer,
    CategorySerializer, GenreSerializer
)

# from rest_framework import filters
# from rest_framework import mixins
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from api.permissions import IsAuthorOrReadOnly, IsAdmin
# from api.permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from api.pagination import PostsPagination


# class GroupViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


from api.permissions import IsAdmin

class CategoryViewSet(viewsets.ModelViewSet):
    quryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
    # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
        # Вернем обновленный перечень используемых пермишенов
            return (AllowAny,)
    # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions() 

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin,)
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
