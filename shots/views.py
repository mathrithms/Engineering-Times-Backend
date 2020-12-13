from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .serializers import CategoryListSerializer, ShotsListSerializer
from .models import Category, Shots


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class RecommendedListView(ListAPIView):
    queryset = Shots.objects.filter(is_recommended=True)
    serializer_class = ShotsListSerializer
    pagination_class = PageNumberPagination


class ShotsCategoryListView(ListAPIView):
    serializer_class = ShotsListSerializer
    pagination_class = PageNumberPagination

    def get(self, request, id, *args, **kwargs):
        try:
            self.queryset = Category.objects.get(id=id).shots.all()
            return self.list(request, *args, **kwargs)

        except Category.DoesNotExist:
            response_object = {
                'error': 'category ' + str(id) + ' not found',
            }
            return Response(response_object, status=HTTP_404_NOT_FOUND)
