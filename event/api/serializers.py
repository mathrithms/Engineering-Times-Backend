from rest_framework import serializers
from event.models import Event
# ModelSerializer


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['title', 'time', 'cost', 'description',
                  'link', 'image', 'organizers', 'type']
