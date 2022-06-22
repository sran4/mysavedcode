
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('codes-examples/', views.notes, name='notes'),
    path('favourites-codes-examples/', views.favs_notes, name='favs-notes'),
    path('add_code/', views.create_note, name='create-note'),
    path('update_code/<int:pk>', views.update_note, name='update-note'),
    path('delete_code/<int:pk>', views.delete_note, name='delete-note'),
    # path('notes_detail/<int:pk>',
    #      views.NotesDetailView.as_view(), name='notes_detail'),
    path('Code_Detail/<int:code_id>/',
         views.NotesDetailView, name='notes_detail'),

    path('assemblies/', views.homework, name='home-work'),
    path('create-assembly/', views.create_assembly, name='create-assembly'),
    path('complete-assembly/<int:pk>',
         views.complete_homework, name='complete-homework'),
    path('update-assembly/<int:pk>', views.update_homework, name='update-homework'),
    path('delete-assembly/<int:pk>', views.delete_homework, name='delete-homework'),

    path('youtube/', views.youtube, name='youtube'),

    path('todos/', views.todo, name='todo'),
    path('update-todo/<int:pk>', views.update_todo, name='update-todo'),
    path('delete-todo/<int:pk>', views.delete_todo, name='delete-todo'),

    path('books/', views.books, name='books'),
    path('dictionary/', views.dictionary, name='dictionary'),

    path('wikipedia/', views.wiki, name='wiki'),
    path('conversion/', views.conversion, name='conversion'),
]
