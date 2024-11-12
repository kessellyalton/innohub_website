from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
import logging
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from .forms import EmailPostForm, ContactForm, UploadFileForm, PDFFileForm
from .models import Blog, Resume, PDFFile,Testimonial,Portfolio, Blog,BlogPost,Article
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'portfolio/home.html')

def about(request):
    return render(request, 'portfolio/about.html')  # Add this view

def projects(request):
    # Render a simple template for now
    portfolios = Portfolio.objects.all()
    return render(request, 'portfolio/portfolio_list.html', {'portfolios': portfolios})


def contact(request):
    # Render a simple template for now
    return render(request, 'portfolio/contact.html')


def get_started(request):
    return render(request, 'portfolio/get_started.html')

def learn_more(request):
    return render(request, 'portfolio/learn_more.html')




def portfolio_list(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'portfolio/portfolio_list.html', {'portfolios': portfolios})

def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    return render(request, 'portfolio/portfolio_detail.html', {'portfolio': portfolio})

# Blog List View
def blog(request):
    posts = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'portfolio/blog_list.html', {'posts': posts})

# Blog Detail View
def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'portfolio/blog_detail.html', {'post': post})

def post_share(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Build the email content
            subject = f"{cd['name']} recommends you read '{post.title}'"
            message = f"Read '{post.title}' at {request.build_absolute_uri(post.get_absolute_url())}\n\n" \
                      f"{cd['name']}’s message:\n{cd['message']}"
            send_mail(subject, message, 'your_email@example.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'portfolio/post_share.html', {
        'post': post,
        'form': form,
        'sent': sent
    })


def post_share(request, post_id):
    post_1 = get_object_or_404(Blog, pk=post_id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post_1.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post_1.title}"
            message = f"Read {post_1.title} at {post_url}\n\n{cd['name']}\'s comments: {cd.get('comments', '')}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])

            # Set the flash message
            messages.success(request,
                             "Thank you for getting in touch. Your message is well received. I will get back to you soon.")

            # Redirect to thank you page
            return redirect('thank_you')  # Assumes 'thank_you' is defined in urls.py

    else:
        form = EmailPostForm()

    return render(request, 'portfolio/post_share.html', {'form': form, 'post': post_1, 'sent': sent})





def upload_resume(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = UploadFileForm()
    return render(request, 'portfolio/upload.html', {'form': form})


def upload_success(request):
    return render(request, 'portfolio/upload_success.html')

def resume_view(request):
    return render(request, 'portfolio/resume.html')



def testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'portfolio/testimonials.html', {'testimonials': testimonials})




def thank_you(request):
    return render(request, 'portfolio/thank_you.html')

def submit_form_1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"From: {name}\nEmail: {email}\n\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['kessellyalton1@gmail.com'],
                fail_silently=False,
            )
            return redirect('thank_you')
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return render(request, 'portfolio/contact.html', {'error_message': 'There was an error sending your email. Please try again later.'})

    return render(request, 'portfolio/contact.html')

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list')
    else:
        form = PDFFileForm()
    return render(request, 'upload_pdf.html', {'form': form})

def pdf_list(request):
    pdfs = PDFFile.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})

def download_pdf(request, pk):
    pdf = get_object_or_404(PDFFile, pk=pk)
    response = HttpResponse(pdf.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf.file.name}"'
    return response






def press_view(request):
    featured_post = Article.objects.filter(is_featured=True).first()  # Get the first featured article
    top_stories = Article.objects.exclude(id=featured_post.id if featured_post else None)[:3]  # Exclude featured from top stories if present

    # Dictionary of articles by category, limited to 3 per category for display
    sections = {
        'News & Updates': Article.objects.filter(category='news_updates')[:3],
        'Educational Content': Article.objects.filter(category='educational')[:3],
        'Promotions & Offers': Article.objects.filter(category='promotions')[:3],
        'Thought Leadership & Insights': Article.objects.filter(category='thought_leadership')[:3],
        'Community & Engagement': Article.objects.filter(category='community')[:3],
        'Lifestyle & Inspiration': Article.objects.filter(category='lifestyle')[:3],
        'Curated Content & Roundups': Article.objects.filter(category='curated')[:3],
        'Behind-the-Scenes & Company Culture': Article.objects.filter(category='behind_scenes')[:3],
        'Seasonal & Thematic Newsletters': Article.objects.filter(category='seasonal')[:3],
        'Feedback & Surveys': Article.objects.filter(category='feedback')[:3],
        'Sports & Entertainment': Article.objects.filter(category='sport')[:3],
    }

    context = {
        'featured_post': featured_post,
        'top_stories': top_stories,
        'sections': sections,
    }

    return render(request, 'portfolio/press.html', context)

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    related_articles = Article.objects.filter(category=article.category).exclude(id=article_id)[:4]
    return render(request, 'portfolio/article_detail.html', {
        'article': article,
        'related_articles': related_articles,
    })


def category_articles(request, category_name):
    # Find the human-readable name for the category
    category_display_name = dict(Article.CATEGORY_CHOICES).get(category_name, category_name.replace("_", " ").title())

    # Filter articles by the selected category
    articles = Article.objects.filter(category=category_name).order_by('-date_posted')
    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category_name': category_display_name,  # Use the display name in the context
    }
    return render(request, 'portfolio/category_articles.html', context)

class ThankYouView(TemplateView):
    template_name = "portfolio/thank_you.html"

def documents(request):
    return render(request, 'portfolio/documents.html')  # Add this view


def documents_view(request):
    resumes = Resume.objects.all()
    pdfs = PDFFile.objects.all()
    context = {
        'resumes': resumes,
        'pdfs': pdfs,
    }
    return render(request, 'portfolio/documents.html', context)

def download_resume(request, pk):
    try:
        resume = get_object_or_404(Resume, pk=pk)
        file_path = os.path.join(settings.MEDIA_ROOT, resume.file.name)

        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, content_type='application/pdf')
        else:
            logger.error(f"File not found: {file_path}")
            return HttpResponse("File not found", status=404)
    except Resume.DoesNotExist:
        logger.error("No resume found with the given id")
        return HttpResponse("No resume found", status=404)
    except Exception as e:
        logger.error(f"Error opening file: {e}")
        return HttpResponse("Error opening file", status=500)
