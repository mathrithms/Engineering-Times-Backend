from .models import Blog, Recommended
from rest_framework.views import APIView
from .serializers import (
    BlogDetailSerializer,
    BlogListSerializer,
    RecommendedSerializer
)
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view


class BlogDetailsView(APIView):
    def get(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
            serializer = BlogDetailSerializer(blog)
            return Response(serializer.data)

        except Blog.DoesNotExist:
            response_object = {
                'error': 'blog ' + str(id) + ' not found',
            }
            return Response(response_object, status=HTTP_404_NOT_FOUND)


class BlogsListView(ListAPIView):
    serializer_class = BlogListSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        recommended = Recommended.objects.first()

        if recommended is None:
            return Blog.objects.all()
        else:
            return Blog.objects.exclude(
                id__in=[
                    recommended.tier1.id,
                    recommended.tier2.id,
                    recommended.tier3.id,
                    recommended.tier4.id
                ])


@api_view(['GET'])
def featured(request):
    if request.method == 'GET':
        recommended = Recommended.objects.first()
        serializer = RecommendedSerializer(recommended)
        return Response(serializer.data)
