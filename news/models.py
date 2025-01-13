from django.db import models
from django.utils.text import slugify
from markitup.fields import MarkupField


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=250)
    content = MarkupField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='static/images/')
    image_min = models.FileField(upload_to='static/images/')
    alt = models.CharField(max_length=30)
    categories = models.ManyToManyField('Category', related_name='posts')
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
