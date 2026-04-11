from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text='Выберите дату и время публикации'
    )
    class Meta:
        model = Post
        fields = ['title', 'text', 'location', 'category', 'image', 'pub_date']