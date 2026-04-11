from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy

User = get_user_model()

def index(request):
    current_time = timezone.now()

    response = 'blog/index.html'

    post_list = Post.objects.select_related('category').filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
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
    paginator = Paginator(category_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj
    }

    return render(request, response, context)

def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author=user_profile,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile':user_profile,
        'page_obj':page_obj
    }
    return render(request, 'blog/profile.html', context)

class CreatePostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'location', 'category', 'image']
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'location', 'category', 'image', 'pub_date']
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.id})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})