from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DocumentationArticle, BlogPost, DocumentationSection
from .serializers import DocumentationArticleSeriazlier, BlogPostSeriazlier, DocumentationSectionSerializer, DocumentationSectionsCountSerializer
from django.db.models import Q
from django.core import serializers
from django.db.models import Count

class DocumentationArticlesView(APIView):
    def get(self, request):
        data = request.query_params
        section = data.get('section')
        search = data.get('search')
        articles = DocumentationArticle.objects.all()

        if (search):
           articles = articles.filter(Q(header__icontains = search) | Q(content__icontains = search))

        sections = DocumentationSection.objects.all()
        sections_with_counts = DocumentationSection.objects.filter(documentationarticle__in=articles).annotate(article_count=Count('documentationarticle'))
        sections_count_serializer = DocumentationSectionsCountSerializer(sections_with_counts, many=True)
        
        if (section):
           articles = articles.filter(section__pk = section)
        serializer = DocumentationArticleSeriazlier(articles, many=True)

        counts = {obj["name"]: obj["article_count"] for obj in [dict(item) for item in sections_count_serializer.data]}

        return Response({ 'articles': serializer.data, 'counts': counts })
    
class DocumentationArticleView(APIView):
    def get(self, request, id=None):
        try:
          article = DocumentationArticle.objects.get(pk=id)
          serializer = DocumentationArticleSeriazlier(article)
          return Response(serializer.data)
        except:
          return Response(status=404)
        
class BlogPostsView(APIView):
    def get(self, request):
        data = request.query_params
        search = data.get('search')
        articles = BlogPost.objects.all()
        
        if (search):
           articles = articles.filter(Q(title__icontains = search) | Q(content__icontains = search))

        serializer = BlogPostSeriazlier(articles, many=True)
        return Response(serializer.data)
    
class BlogPostView(APIView):
    def get(self, request, id=None):
        try:
          article = BlogPost.objects.get(pk=id)
          serializer = BlogPostSeriazlier(article)
          return Response(serializer.data)
        except:
          return Response(status=404)
        
class DocumentationSections(APIView):
    def get(self, request):
        sections = DocumentationSection.objects.all()

        serializer = DocumentationSectionSerializer(sections, many=True)

        return Response(serializer.data)