from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


class CategoryANDGenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Родительский класс для GenreViewset и CategoryViewSet"""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
