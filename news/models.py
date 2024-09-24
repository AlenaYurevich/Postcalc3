from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='static/images/')
    image_min = models.FileField(upload_to='static/images/')
    alt = models.CharField(max_length=30)
    categories = models.ManyToManyField('Category', related_name='posts')

    def __str__(self):
        return self.title
