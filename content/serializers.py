from rest_framework import serializers
from .models import DocumentationArticle, DocumentationSection, BlogPost, Tag

class DocumentationSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentationSection
        fields = '__all__'

class DocumentationSectionsCountSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    article_count = serializers.IntegerField()

class DocumentationArticleSeriazlier(serializers.ModelSerializer):
    section = DocumentationSectionSerializer(read_only=True)

    class Meta:
        model = DocumentationArticle
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BlogPostSeriazlier(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = BlogPost
        fields = '__all__'