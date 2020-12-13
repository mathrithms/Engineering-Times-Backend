from django.contrib import admin
from .models import Blog, ContentBlock, Author, Reference, Recommended


class ContentBlockTabularInline(admin.TabularInline):
    model = ContentBlock


class ReferenceTabularInline(admin.TabularInline):
    model = Reference


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']

    class Meta:
        model = Author


class BlogAdmin(admin.ModelAdmin):
    inlines = [ContentBlockTabularInline, ReferenceTabularInline]
    search_fields = ['title', 'id']
    autocomplete_fields = ['author']
    list_display = ['title', 'timestamp', 'id']

    class Meta:
        model = Blog


class RecommendedAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tier1', 'tier2', 'tier3', 'tier4']

    class Meta:
        model = Recommended

    def has_add_permission(self, request):
        if Recommended.objects.count() == 0:
            return True
        else:
            return False


admin.site.register(Blog, BlogAdmin)
admin.site.register(Recommended, RecommendedAdmin)
admin.site.register(Author, AuthorAdmin)
