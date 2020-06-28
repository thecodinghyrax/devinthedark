from django.contrib import admin
from .models import Post, Topic

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_image', 'date_posted')

admin.site.register(Post, PostAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'icon')

admin.site.register(Topic, TopicAdmin)