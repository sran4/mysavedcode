from django.contrib import admin
from .models import Homework, Notes, Todo
# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'language ', 'slug', 'created_at', 'updated_at')


admin.site.register(Notes, NoteAdmin)
admin.site.register(Homework)
admin.site.register(Todo)
