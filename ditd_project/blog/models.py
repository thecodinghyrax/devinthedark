from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Topic(models.Model):
    topic = models.CharField(max_length=30)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.topic



class Post(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    content = RichTextUploadingField(blank=False, 
                                        null=False,
                                        external_plugin_resources=[(
                                        'youtube',
                                        '/static/blog/ckeditor_plugins/youtube/youtube_2.1.14/youtube/',
                                        'plugin.js'
                                        ),(
                                        'wordcount',
                                        '/static/blog/ckeditor_plugins/wordcount/wordcount_1.17.6/wordcount/',
                                        'plugin.js'                                        
                                        )],
                                        )
    article_image = RichTextUploadingField(blank=True, null=True, config_name='image')
    date_posted = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)


    def __str__(self):
        return self.title

    # this is used once a post is create successfully.
    # reverse will send the full url of a route back as a string as opposed to 
    # redirect which will actually send the user to another page
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_post_topics(self):
        topics = {}

        for num, topic in enumerate(self.topics.all()):
            topics[num] = [topic.icon, topic.topic]
        return topics
