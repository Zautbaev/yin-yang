from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import NewsPost, TeamMember, AboutPage


def _get_about():
    return AboutPage.objects.first()


def index(request):
    latest_news = NewsPost.objects.filter(is_published=True)[:6]
    about = _get_about()
    return render(request, 'modteam/index.html', {
        'latest_news': latest_news,
        'about': about,
    })


def news_list(request):
    posts = NewsPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    about = _get_about()
    return render(request, 'modteam/news_list.html', {
        'page_obj': page_obj,
        'about': about,
    })


def news_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, is_published=True)
    about = _get_about()
    return render(request, 'modteam/news_detail.html', {
        'post': post,
        'about': about,
    })


def about(request):
    about_page = _get_about()
    members = TeamMember.objects.all()
    return render(request, 'modteam/about.html', {
        'about': about_page,
        'members': members,
    })
