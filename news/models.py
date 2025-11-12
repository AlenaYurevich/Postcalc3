from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250)
    # content = models.RichTextField(max_length=2000, blank=True)
    content = RichTextField(config_name='awesome_ckeditor')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='static/images/')
    image_min = models.FileField(upload_to='static/images/')
    alt = models.CharField(max_length=30)
    categories = models.ManyToManyField('Category', related_name='posts')
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
