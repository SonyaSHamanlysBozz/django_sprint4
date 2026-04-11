from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.utils import timezone

User = get_user_model()

def index(request):
    current_time = timezone.now()

    response = 'blog/index.html'

    post_list = Post.objects.select_related('category').filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {
        'post_list': post_list
    }

    return render(request, response, context)


def post_detail(request, post_id):
    current_time = timezone.now()

    response = 'blog/detail.html'
    publication = get_object_or_404(
        Post.objects.filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        ),
        id=post_id
    )
    context = {
        'post': publication
    }
    return render(request, response, context)


def category_posts(request, category_slug):
    current_time = timezone.now()
    response = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    category_posts = Post.objects.select_related('category').filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lte=current_time
    )
    context = {
        'category': category,
        'post_list': category_posts
    }

    return render(request, response, context)

def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    context = [
        'profile':user_profile
    ]
    return render(request, 'blog/profile.html', context)