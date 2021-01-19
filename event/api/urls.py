from django.urls import path
from .views import (
    EventListView,
    FeaturedListView,
    EventListByYearMonth,
    EventListByDateYearMonth,
)

app_name = 'event'

urlpatterns = [
    path('top', FeaturedListView.as_view(), name="top"),
    path('', EventListView.as_view(), name="list"),
    path('<int:month>/<int:year>/',
         EventListByYearMonth.as_view(), name="month"),
    path('<int:date>/<int:month>/<int:year>/',
         EventListByDateYearMonth.as_view(), name="date"),
]
