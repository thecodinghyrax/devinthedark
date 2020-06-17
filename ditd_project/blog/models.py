from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    preview = RichTextField(external_plugin_resources=[(
                                        'wordcount',
                                        '/static/blog/ckeditor_plugins/wordcount/wordcount_1.17.6/wordcount/',
                                        'plugin.js'                                        
                                        )],
                                        config_name='preview')
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


    def __str__(self):
        return self.title

    # this is used once a post is create successfully.
    # reverse will send the full url of a route back as a string as opposed to 
    # redirect which will actually send the user to another page
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

# class Tag(modles.Model):
#     tag = modles.CharField(max_length=30, blank=True, null=True)

#     def __str__(self):
#         return self.tag

#I getting tired but I think I need to make a table of tags and then 
# have a one-to-many (ForignKey) relationship from Post to Tag
# Need to work out how select from the tag table to use in the Post