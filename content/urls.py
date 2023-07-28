from django.contrib import admin
from django.urls import path, include
from content import views

urlpatterns = [
    path('documentation/articles', views.DocumentationArticlesView.as_view(), name='documentation-articles'),
    path('documentation/articles/<int:id>', views.DocumentationArticleView.as_view(), name='documentation-article'),
    path('documentation/sections', views.DocumentationSections.as_view(), name='documentation-sections'),
    path('blog/posts', views.BlogPostsView.as_view(), name='blog-posts'),
    path('blog/posts/<int:id>', views.BlogPostView.as_view(), name='blog-post'),
]
