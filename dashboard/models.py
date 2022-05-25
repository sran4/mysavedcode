from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=200)
    # code_here = RichTextField(blank=True)
    code_here = RichTextUploadingField(config_name='portal_config')
    notes_for_yourself = models.TextField()
    fav = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"

    def noted(self):
        return self.notes_for_yourself[:285]

    def __str__(self):
        return self.language


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
