from django.contrib import admin
from django.urls import path, include
from content import views

urlpatterns = [
    path('documentation/articles', views.DocumentationArticlesView.as_view()),
    path('documentation/articles/<int:id>', views.DocumentationArticleView.as_view()),
    path('documentation/sections', views.DocumentationSections.as_view()),
    path('blog/posts', views.BlogPostsView.as_view()),
    path('blog/posts/<int:id>', views.BlogPostView.as_view()),
]
