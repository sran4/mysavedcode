from django.contrib import admin
from .models import Homework, Notes, Category, Todo
# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'slug', 'created_at', 'updated_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(Notes, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Homework)
admin.site.register(Todo)
