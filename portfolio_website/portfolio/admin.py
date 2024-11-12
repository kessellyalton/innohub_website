from django.contrib import admin
from .models import Portfolio

from .models import Blog, Contact, Resume, PDFFile,Testimonial, Article, Category


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project_date')
    search_fields = ('title', 'category')
    list_filter = ('category',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'created_at', 'updated_at')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'author_title', 'created_at']
    search_fields = ['author_name', 'quote']






@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    search_fields = ['name', 'email', 'subject']

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['file', 'description', 'uploaded_at']
    search_fields = ['description']

@admin.register(PDFFile)
class PDFFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']




@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'category')
    search_fields = ('title', 'content')
    list_filter = ('category', 'date_posted')
    ordering = ('-date_posted',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']