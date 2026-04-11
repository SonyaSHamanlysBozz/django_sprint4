from django.urls import path, include
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts,
         name='category_posts'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('posts/create/', views.CreatePostCreateView.as_view(), name='create_post')
]
