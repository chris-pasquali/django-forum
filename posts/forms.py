from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

class CreatePost(ModelForm):
  class Meta:
    model = Post
    fields = '__all__'
    exclude = ['user_profile']

class CommentForm(ModelForm):
  content = forms.CharField(label='', widget=forms.Textarea(attrs={
    'class': 'form-control',
    'placeholder': 'Type your comment',
    'id': 'usercomment',
    'rows': '3'
  }))
  class Meta:
    model = Comment
    fields = ('content',)

class UserProfileForm(ModelForm):
  class Meta:
    model = UserProfile
    # fields = '__all__'
    fields = ['first_name', 'last_name', 'phone', 'email', 'profile_picture',]
    exclude = ['user']