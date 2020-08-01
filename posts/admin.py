from django.contrib import admin
from .models import *

admin.site.register(PostView)
admin.site.register(UserProfile)
admin.site.register(Car)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Post)

