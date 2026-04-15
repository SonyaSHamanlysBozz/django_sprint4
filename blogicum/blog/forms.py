from django import forms
from .models import Post, Comments
from django.contrib.auth import get_user_model

User = get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'location', 'category', 'image', 'pub_date']
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            )
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text', )

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']