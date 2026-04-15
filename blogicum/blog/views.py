from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comments
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .forms import CommentsForm, ProfileEditForm, PostForm
from django.db.models import Count
from django.contrib.auth import logout
from django.http import Http404

User = get_user_model()


def index(request):
    current_time = timezone.now()

    response = 'blog/index.html'

    post_list = Post.objects.select_related('category').filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }

    return render(request, response, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user != post.author:
        is_published = (
            post.is_published and 
            post.category.is_published and 
            post.pub_date <= timezone.now()
        )
        if not is_published:
            raise Http404
        
    comment_form = CommentsForm()
    comments = post.comments.all()
    context = {
        'post': post,
        'form': comment_form,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


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
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
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
    posts = Post.objects.filter(author=user_profile)
    
    if request.user.username != username:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
        
    posts = posts.annotate(comment_count=Count('comments')).order_by('-pub_date')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile': user_profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class CreatePostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', post_id=post.id)
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.id})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', post_id=post.id)
        return super().dispatch(request, *args, **kwargs)
    success_url = reverse_lazy('blog:index')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentsUpdateView(LoginRequiredMixin, UpdateView):
    model = Comments
    fields = ['text']
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return redirect('blog:post_detail', post_id=comment.post.id)
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.post.id})

class CommentsDeleteView(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return redirect('blog:post_detail', post_id=comment.post.id)
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.post.id})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})

def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')