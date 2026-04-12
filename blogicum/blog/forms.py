from django import forms
from .models import Post, Comments
from django.contrib.auth import get_user_model

User = get_user_model()

class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text='Выберите дату и время публикации'
    )
    class Meta:
        model = Post
        fields = ['title', 'text', 'location', 'category', 'image', 'pub_date']

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text', )

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']