from django.urls import path
from .views import CategoryListView, RecommendedListView, ShotsCategoryListView

urlpatterns = [
    path('category/list/', CategoryListView.as_view()),
    path('category/<int:id>/', ShotsCategoryListView.as_view()),
    path('', RecommendedListView.as_view()),
]
