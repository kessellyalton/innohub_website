# portfolio/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='portfolio-list'),  # New URL for 'projects'

    path('blog/', views.blog, name='blog-list'),  # New URL for 'blog'

    path('contact/', views.contact, name='contact'),  # New contact URL
    path('get-started/', views.get_started, name='get_started'),
    path('learn-more/', views.learn_more, name='learn_more'),
    path('about/', views.about, name='about'),  # Add this line

    path('portfolio/', views.portfolio_list, name='portfolio-list'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio-detail'),
    path('<int:pk>/', views.portfolio_detail, name='portfolio-detail'),

    path('blog/<int:pk>/', views.blog_detail, name='blog-detail'),
    path('blog/<int:pk>/share/', views.post_share, name='post_share'),





    path('resume/', views.resume_view, name='resume'),




    path('testimonials/', views.testimonials, name='testimonials'),

    path('contact/', views.contact, name='contact'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('submit_form_1/', views.submit_form_1, name='submit_form_1'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('download/', views.download_resume, name='download_resume'),
    path('upload/success/', views.upload_success, name='upload_success'),


    path('login/', auth_views.LoginView.as_view(template_name='mysite/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mysite/logout.html'), name='logout'),




    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('pdfs/', views.pdf_list, name='pdf_list'),
    path('download/<int:pk>/', views.download_pdf, name='download_pdf'),





    path('press/', views.press_view, name='press-home'),
    path('press/article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('press/category/<str:category_name>/', views.category_articles, name='category_articles'),

    path('documents/', views.documents_view, name='documents'),
    path('download_resume/<int:pk>/', views.download_resume, name='download_resume'),
    path('download_pdf/<int:pk>/', views.download_pdf, name='download_pdf'),
]


