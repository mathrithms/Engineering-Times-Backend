from rest_framework import serializers
from .models import Author, Blog, Reference, ContentBlock, Recommended


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'thumbnail']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'description', 'profile']


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['title', 'link']


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ['text', 'image']


class BlogDetailSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField('get_content')
    author = serializers.SerializerMethodField('get_author')
    references = serializers.SerializerMethodField('get_references')

    class Meta:
        model = Blog
        fields = ['title', 'abstract', 'thumbnail', 'main_image', 'content', 'author', 'references']

    def get_content(self, blog):
        return ContentBlockSerializer(blog.contentBlock.all(), many=True).data

    def get_author(self, blog):
        return AuthorSerializer(blog.author).data

    def get_references(self, blog):
        return ReferenceSerializer(blog.references.all(), many=True).data


class BlogRecommendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title']


class RecommendedSerializer(serializers.ModelSerializer):
    tier1 = serializers.SerializerMethodField('get_blog1')
    tier2 = serializers.SerializerMethodField('get_blog2')
    tier3 = serializers.SerializerMethodField('get_blog3')
    tier4 = serializers.SerializerMethodField('get_blog4')

    class Meta:
        model = Recommended
        fields = ['tier1', 'tier1_image', 'tier2', 'tier2_image', 'tier3', 'tier3_image', 'tier4', 'tier4_image']

    def get_blog1(self, recommended):
        return BlogRecommendedSerializer(recommended.tier1).data

    def get_blog2(self, recommended):
        return BlogRecommendedSerializer(recommended.tier2).data

    def get_blog3(self, recommended):
        return BlogRecommendedSerializer(recommended.tier3).data

    def get_blog4(self, recommended):
        return BlogRecommendedSerializer(recommended.tier4).data
