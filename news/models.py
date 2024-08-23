from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=30, default="no_title")
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='calc/static/images/gallery')
    image_min = models.FileField(upload_to='calc/static/images/gallery')
    alt = models.CharField(max_length=30)
    categories = models.ManyToManyField('Category', related_name='posts')

    def __str__(self):
        return self.title
