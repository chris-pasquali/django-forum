from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class PostView(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey('Post', on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username

class UserProfile(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=200, null=True)
  last_name = models.CharField(max_length=200, null=True)
  phone = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200, null=True)
  profile_picture = models.ImageField(default="profile1.png", null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True)

  @property
  def full_name(self):
    return '{0} {1}'.format(self.first_name, self.last_name)
    # return full_name.title()

  # @property
  # def username(self):
  #   return user.username
  
  def __str__(self):
    return self.full_name
    #return self.user.username

class Car(models.Model):
  TRANSMISSION = (
        ('Automatic', 'Automatic'),
        ('Manual', ' Manual'),
    )
  make = models.CharField(max_length=150)
  model = models.CharField(max_length=150)
  badge = models.CharField(max_length=150, null=True, blank=True)
  year = models.CharField(max_length=5, null=True, blank=True)
  transmission = models.CharField(max_length=50, choices=TRANSMISSION, blank=True, null=True)

  def __str__(self):
    return self.make + '' + self.model

class Tag(models.Model):
  title = models.CharField(max_length=30, null=True)

  def __str__(self):
    return self.title

class Comment(models.Model):
  # user = models.ForeignKey(User, on_delete=models.CASCADE)
  user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  content = models.TextField()
  post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

  def __str__(self):
    # return self.user_profile.user.username
    return self.post.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    # overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post_image = models.ImageField(null=True, blank=True)
    # comment_count = models.IntegerField(default = 0)
    # view_count = models.IntegerField(default = 0)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    # up_vote
    # down_vote
  
    def __str__(self):
      return self.title

    def get_absolute_url(self):
      return reverse('post-detail', kwargs={
        'pk': self.pk
      })

    def get_update_url(self):
      return reverse('post-update', kwargs={
        'pk': self.pk
      })

    def get_delete_url(self):
      return reverse('post-delete', kwargs={
        'pk': self.pk
      })

    @property
    def get_comments(self):
      return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
      return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
      return PostView.objects.filter(post=self).count()
