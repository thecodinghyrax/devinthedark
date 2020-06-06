from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    content = RichTextUploadingField(blank=False, null=False)
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