from django.contrib import admin
from .models import Category, Shots


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title']

    class Meta:
        model = Category


class ShotsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'timestamp', 'id']
    autocomplete_fields = ['category']
    search_fields = ['title']

    class Meta:
        model = Shots


admin.site.register(Shots, ShotsAdmin)
admin.site.register(Category, CategoryAdmin)
