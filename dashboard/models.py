from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

import random
import string
from django.utils.text import slugify
from django.db.models.signals import pre_save


def random_string_generator(size=10, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    Just change the '_name' line below to fit your needs.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.language)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('notes_by_category', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=130, blank=True, null=True, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=200,)
    # code_here = RichTextField(blank=True)
    code_here = RichTextUploadingField(config_name='portal_config')
    notes_for_yourself = models.TextField()
    fav = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']
        verbose_name = "notes"
        verbose_name_plural = "notes"

    # def noted(self):
    #     return self.notes_for_yourself[:80]
    def get_url(self):
        return reverse('notes_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.language


def Notes_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(Notes_pre_save_receiver, sender=Notes)


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.CharField(max_length=50)
    assembly = models.CharField(max_length=50)
    qty = models.PositiveIntegerField()
    comments = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "homework"
        verbose_name_plural = "homework"

    def __str__(self):
        return self.assembly


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "todo"
        verbose_name_plural = "todo"

    def __str__(self):
        return self.title
