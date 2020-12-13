from .models import Intern, Job
from .serializers import InternSerializer, JobSerializer
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
import pytz


class InternListView(ListAPIView):
    serializer_class = InternSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        tz = 'Asia/Kolkata'
        timezone.activate(pytz.timezone(tz))
        queryset = Intern.objects.filter(expire__gte=timezone.now())
        return queryset


class JobListView(ListAPIView):
    serializer_class = JobSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        tz = 'Asia/Kolkata'
        timezone.activate(pytz.timezone(tz))
        queryset = Job.objects.filter(expire__gte=timezone.now())
        return queryset
