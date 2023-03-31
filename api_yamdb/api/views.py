from rest_framework import viewsets, filters 
from rest_framework.permissions import AllowAny


from reviews.models import Genre, Category
from .serializers import (GenreSerializer, CategorySerializer)
from api.permissions import IsSuperUserIsAdminIsAnonim

class CategoryViewSet(viewsets.ModelViewSet):
    quryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsSuperUserIsAdminIsAnonim, )
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
    permission_classes = (IsSuperUserIsAdminIsAnonim,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (AllowAny,)
        return super().get_permissions() 
