from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import InShotsAds


class InShotsAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = InShotsAds
        fields = ['title', 'text', 'image', 'link']


@api_view(['GET'])
def InShotsAdView(request):
    if request.method == 'GET':
        ads = InShotsAds.objects.first()
        serializers = InShotsAdSerializer(ads)
        return Response(serializers.data)
