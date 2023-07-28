from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import DocumentationArticle, BlogPost, DocumentationSection
from .serializers import Tag

class DocumentationArticlesViewTests(APITestCase):
    def setUp(self):
        self.section1 = DocumentationSection.objects.create(name='Section 1')
        self.section2 = DocumentationSection.objects.create(name='Section 2')

        self.article1 = DocumentationArticle.objects.create(
            header='Article 1',
            content='Content for Article 1',
            section=self.section1
        )

        self.article2 = DocumentationArticle.objects.create(
            header='Article 2',
            content='Content for Article 2',
            section=self.section2
        )

    def test_get_documentation_articles_without_search_and_section(self):
        url = reverse('documentation-articles')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_documentation_articles_with_search(self):
        url = reverse('documentation-articles')
        data = {'search': 'Article 1'}
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_documentation_articles_with_section(self):
        url = reverse('documentation-articles')
        data = {'section': self.section1.pk}
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DocumentationArticleViewTests(APITestCase):
    def setUp(self):
        self.section = DocumentationSection.objects.create(name='Section')
        self.article = DocumentationArticle.objects.create(
            header='Test Article',
            content='Content for Test Article',
            section=self.section
        )

    def test_get_documentation_article_success(self):
        url = reverse('documentation-article', args=[self.article.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_documentation_article_not_found(self):
        url = reverse('documentation-article', args=[9999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class BlogPostsViewTests(APITestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='Tag 1')
        self.tag2 = Tag.objects.create(name='Tag 2')

        self.post1 = BlogPost.objects.create(
            title='Post 1',
            content='Content for Post 1',
            author='Author 1',
            date_published='2023-07-28'
        )
        self.post1.tags.add(self.tag1, self.tag2)

        self.post2 = BlogPost.objects.create(
            title='Post 2',
            content='Content for Post 2',
            author='Author 2',
            date_published='2023-07-29'
        )
        self.post2.tags.add(self.tag2)

    def test_get_blog_posts_without_search(self):
        url = reverse('blog-posts')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_blog_posts_with_search(self):
        url = reverse('blog-posts')
        data = {'search': 'Post 1'}
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BlogPostViewTests(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Tag')
        self.post = BlogPost.objects.create(
            title='Test Post',
            content='Content for Test Post',
            author='Author',
            date_published='2023-07-28'
        )
        self.post.tags.add(self.tag)

    def test_get_blog_post_success(self):
        url = reverse('blog-post', args=[self.post.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_blog_post_not_found(self):
        url = reverse('blog-post', args=[9999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class DocumentationSectionsTests(APITestCase):
    def setUp(self):
        self.section1 = DocumentationSection.objects.create(name='Section 1')
        self.section2 = DocumentationSection.objects.create(name='Section 2')

    def test_get_documentation_sections(self):
        url = reverse('documentation-sections')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
