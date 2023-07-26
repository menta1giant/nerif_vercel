from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    date_published = models.DateField()
    tags = models.ManyToManyField(Tag, blank=True)
    cover = models.ImageField(default='', upload_to='blog/covers/')

    def __str__(self):
        return self.title
    
class DocumentationSection(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class DocumentationArticle(models.Model):
    header = models.CharField(max_length=200)
    content = models.TextField()
    section = models.ForeignKey(DocumentationSection, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.header