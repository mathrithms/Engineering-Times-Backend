from django.urls import path
from .views import BlogDetailsView, BlogsListView, featured

urlpatterns = [
    path('list/', BlogsListView.as_view()),
    path('<int:id>/', BlogDetailsView.as_view()),
    path('featured/', featured)
]
