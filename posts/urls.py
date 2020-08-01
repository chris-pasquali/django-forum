from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  path('', views.home, name="home"),
  path('create/', views.create_post, name="post-create"),
  path('post/<pk>/', views.detail_view, name="post-detail"),
  path('user/<id>/', views.profile_view, name="user-profile"),
]