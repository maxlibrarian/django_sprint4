from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control-file'}
            ),
        }
