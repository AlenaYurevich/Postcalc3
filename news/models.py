from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='images/gallery')
    image_min = models.FileField(upload_to='images/gallery')
    alt = models.CharField(max_length=100)
    categories = models.ManyToManyField('Category', related_name='posts')
