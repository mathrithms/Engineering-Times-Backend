from django.urls import path
from .views import store_view

app_name = 'storage'

urlpatterns = [
    path('store_view/', store_view, name='store_view'),
]
