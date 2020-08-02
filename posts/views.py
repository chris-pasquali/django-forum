from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
# from .filters import *
# from .decorators import unauthenticated_user, allowed_users, admin_only

def get_user_profile(user):
  qs = UserProfile.objects.filter(user=user)
  if qs.exists():
    return qs[0]
  return None

def get_tags_count():
  queryset = Post \
    .objects \
    .values('tags__title') \
    .annotate(Count('tags__title'))
  return queryset

# @unauthenticated_user
def home(request):
  posts = Post.objects.all().order_by('-timestamp') 
  context = {
    'posts': posts
  }
  return render(request, 'home.html', context)

def create_post(request):
  form = CreatePost(request.POST or None, request.FILES or None)
  user_profile = get_user_profile(request.user)
  if request.method == 'POST':
    print('Printing POST:', request.POST)
    if form.is_valid():
      form.instance.user_profile = user_profile
      form.save()
      return redirect(reverse("post-detail", kwargs={
        'id': form.instance.id
      }))
      # return redirect('home')

  context = {
    'form': form
  }
  return render(request, 'create.html', context)

def detail_view(request, pk):
  tags_count = get_tags_count()
  post = get_object_or_404(Post, pk=pk)
  most_recent = Post.objects.order_by('-timestamp')[:5]
  comment_form = CommentForm(request.POST or None)

  # if request.user.is_authenticated:
  #   PostView.objects.get_or_create(user=request.user, post=post)
  
  if request.method == 'POST':
    if comment_form.is_valid():
      comment_form.instance.user = request.user
      comment_form.instance.post = post
      comment_form.save()
      return redirect(reverse("post-detail", kwargs={
        'pk': post.id
      }))
  
  context = {
    'comment_form': comment_form,
    'most_recent': most_recent,
    'tags_count': tags_count,
    'post': post
  }
  return render(request, 'post-detail.html', context)

def profile_view(request, id):
  user_profile = UserProfile.objects.get(id=id)
  no_posts = Post.objects.filter(user_profile=user_profile).count() # finds the number of posts user has created
  posts = Post.objects.filter(user_profile=user_profile) # retreives all posts by user
  no_comments = Comment.objects.filter(user_profile=user_profile).count() 
  comments = Comment.objects.filter(user_profile=user_profile)

  most_recent_post = posts.latest('timestamp')
  recent_post_date = most_recent_post.timestamp
  
  most_recent_comment = comments.latest('timestamp')
  recent_comment_date = most_recent_comment.timestamp

  if recent_post_date > recent_comment_date:
    last_active = recent_post_date
  else:
    last_active = recent_comment_date

  print('most_recent_post - ', recent_post_date)
  print('most_recent_comment - ', recent_comment_date)

  # popular_posts

  context = {
    'user_profile': user_profile,
    'no_posts': no_posts,
    'posts': posts,
    'no_comments': no_comments,
    'comments': comments,
    'last_active': last_active
  }
  return render(request, 'user-profile.html', context)

# @login_required(login_url='login')
def account_settings(request):
  # user_profile = request.user.user_profile
  user_profile = UserProfile.objects.get(user=request.user)
  print(user_profile)
  form = UserProfileForm(instance=user_profile)

  if request.method == 'POST':
    form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
    if form.is_valid():
      form.save()

  posts = Post.objects.filter(user_profile=user_profile) # retreives all posts by user
  comments = Comment.objects.filter(user_profile=user_profile)

  context = {
    'user_profile': user_profile,
    'form': form,
    'posts': posts,
    'comments': comments,
  }
  return render(request, 'account-settings.html', context)

def updatePost(request, pk):
  post = Post.objects.get(id=pk)
  form = CreatePost(instance=post)

  if request.method == 'POST':
    form = CreatePost(request.POST, request.FILES or None, instance=post)
    user_profile = get_user_profile(request.user)
    if form.is_valid():
      form.save()
      return redirect(reverse("post-detail", kwargs={
        'pk': post.id
      }))
      # return redirect("account")
  
  context = {
    'form': form,
  }

  return render(request, 'create.html', context)

def updateComment(request, pk):
  comment = Comment.objects.get(id=pk)
  form = CommentForm(instance=comment)

  if request.method == 'POST':
    form = CommentForm(request.POST, request.FILES or None, instance=comment)
    user_profile = get_user_profile(request.user)
    if form.is_valid():
      form.save()
      return redirect('account')
  
  context = {
    'form': form,
  }
  return render(request, '', context)