from rest_framework import serializers
from .models import Category, Shots


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ShotsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shots
        fields = ['title', 'text', 'image', 'link']
