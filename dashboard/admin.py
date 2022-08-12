from django.contrib import admin
from .models import Homework, Notes, Category, Todo, Tag
# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'fav', 'top',
                    'created_at', 'updated_at')
    search_fields = ['id', 'language', ]
    list_editable = ['fav', 'top', 'language', ]
    list_filter = ('language', 'fav', 'top')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Notes, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Homework)
admin.site.register(Todo)
