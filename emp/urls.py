from django.urls import path
from .views import InternListView, JobListView

urlpatterns = [
    path('interns/', InternListView.as_view()),
    path('jobs/', JobListView.as_view()),
]
