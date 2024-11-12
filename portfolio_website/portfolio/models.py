from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
import bleach
from ckeditor.fields import RichTextField








class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ('consulting', 'Educational Consulting and Leadership'),
        ('research', 'Research, Data Analysis, and Policy Development'),
        ('tech', 'Technology and Digital Platform Development'),
        ('stem', 'STEM Education and International Collaboration'),
    ]

    title = models.CharField(max_length=200)
    description = RichTextField()  # If using CKEditor 4
    # description = CKEditor5Field('Content')  # Uncomment if using CKEditor 5
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='portfolio_images/%Y/%m/%d/')  # Organized by upload date
    client = models.CharField(max_length=100, blank=True, null=True)
    project_date = models.DateField(blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio-detail', args=[str(self.id)])

class Contact(models.Model):
    name = models.CharField(max_length=100, default='John Doe')
    email = models.EmailField(default='example@example.com')
    subject = models.CharField(max_length=200, default='No Subject')
    message = models.TextField(default='No message')
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200, default='Untitled')
    author = models.CharField(max_length=100, default='Anonymous')
    content = CKEditor5Field('Content')
    date_posted = models.DateTimeField(default=timezone.now, blank=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.content = bleach.clean(
            self.content,
            tags=['p', 'strong', 'em', 'a'],
            attributes={'a': ['href', 'title']},
            strip=True
        )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args=[self.pk])


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('news_updates', 'News & Updates'),
        ('educational', 'Educational Content'),
        ('promotions', 'Promotions & Offers'),
        ('thought_leadership', 'Thought Leadership & Insights'),
        ('community', 'Community & Engagement'),
        ('lifestyle', 'Lifestyle & Inspiration'),
        ('curated', 'Curated Content & Roundups'),
        ('behind_scenes', 'Behind-the-Scenes & Company Culture'),
        ('seasonal', 'Seasonal & Thematic Newsletters'),
        ('feedback', 'Feedback & Surveys'),
        ('sport', 'Sports & Entertainment'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    content = CKEditor5Field('Content', config_name='default')
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.pk])


class Testimonial(models.Model):
    quote = CKEditor5Field('Quote', config_name='default')
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} - {self.author_title}"


class Resume(models.Model):
    file = models.FileField(upload_to='uploads/')
    description = models.CharField(max_length=255, blank=True, default='No description provided')
    uploaded_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.file.name


class PDFFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title








# Post model with predefined categories
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Web', 'Web'),
        ('Tech', 'Tech'),
        ('Business', 'Business'),
        ('Health', 'Health'),
        ('Opinion', 'Opinion'),
    ]

    title = models.CharField(max_length=255)
    content = CKEditor5Field('Content', config_name='default')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='press_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    author = models.CharField(max_length=255, blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.pk])

class Testimonial(models.Model):
    quote = CKEditor5Field('Quote ', config_name='default')
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100)
    #author_title= CKEditor5Field('Author Title', config_name='default')
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} - {self.author_title}"

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Article(models.Model):
    CATEGORY_CHOICES = [
        ('news_updates', 'News & Updates'),
        ('educational', 'Educational Content'),
        ('promotions', 'Promotions & Offers'),
        ('thought_leadership', 'Thought Leadership & Insights'),
        ('community', 'Community & Engagement'),
        ('lifestyle', 'Lifestyle & Inspiration'),
        ('curated', 'Curated Content & Roundups'),
        ('behind_scenes', 'Behind-the-Scenes & Company Culture'),
        ('seasonal', 'Seasonal & Thematic Newsletters'),
        ('feedback', 'Feedback & Surveys'),
        ('sport', 'Sports & Entertainment'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    content = CKEditor5Field('Content', config_name='default')
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)  # New field to mark featured articles

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.pk)])