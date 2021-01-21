from event.api.serializers import EventSerializer
from rest_framework.pagination import PageNumberPagination
from event.models import Event, Featured
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
import datetime
from rest_framework import generics


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework.response import Response


class EventListView(ListAPIView):
    date_today = datetime.date.today()
    queryset = Event.objects.filter(time__gte=date_today).order_by('time')
    serializer_class = EventSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)


class FeaturedListView(ListAPIView):
    date_today = datetime.date.today()

    featured = Featured.objects.all().exists()
    if featured:
        queryset = Event.objects.filter(time__gte=date_today)

        def get_queryset(self):
            featured_list = self.queryset.filter(
                featured__event_id__gte=1).order_by('time')
            event_list = self.queryset.filter().exclude(
                featured__event_id__gte=1).order_by('time')[:2]

            return featured_list.union(event_list, all=True)
    else:
        queryset = Event.objects.filter(
            time__gte=date_today).order_by('time')[:3]

    serializer_class = EventSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)


class EventListByYearMonth(generics.ListAPIView):
    serializer_class = EventSerializer
    lookup_month_kwarg = "month"
    lookup_year_kwarg = "year"

    def get_queryset(self):
        month = self.kwargs.get(self.lookup_month_kwarg)
        year = self.kwargs.get(self.lookup_year_kwarg)
        event = Event.objects.filter(
            time__year=year, time__month=month).order_by('time')
        return event


class EventListByDateYearMonth(generics.ListAPIView):
    serializer_class = EventSerializer
    lookup_date_kwarg = "date"
    lookup_month_kwarg = "month"
    lookup_year_kwarg = "year"

    def get_queryset(self):
        date = self.kwargs.get(self.lookup_date_kwarg)
        month = self.kwargs.get(self.lookup_month_kwarg)
        year = self.kwargs.get(self.lookup_year_kwarg)
        event = Event.objects.filter(
            time__day=date,
            time__month=month,
            time__year=year).order_by('time')
        return event
