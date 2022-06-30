from django.contrib.auth.mixins import LoginRequiredMixin
from django import contrib
from django.core.checks import messages
from django.forms.widgets import FileInput
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
# from .models import Notes, Homework
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def home(request):
    return render(request, 'dashboard/home.html')


def handle404(request, exception):
    return render(request, 'dashboard/404.html', )


@login_required
def notes(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    notes = Notes.objects.filter(user=request.user).filter(
        Q(language__icontains=q) |
        Q(notes_for_yourself__icontains=q) |
        Q(code_here__icontains=q)).order_by('-updated_at')
    notes_count = notes.count()
    paginator = Paginator(notes, 40)
    page = request.GET.get('page')
    notes = paginator.get_page(page)
    context = {'notes': notes,
               'notes_count': notes_count,
               }
    return render(request, 'dashboard/notes.html', context)


@login_required
def favs_notes(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    favs = Notes.objects.filter(user=request.user, fav=True).filter(
        Q(language__icontains=q) |
        Q(notes_for_yourself__icontains=q) |
        Q(code_here__icontains=q)).order_by('-updated_at')

    favs_count = favs.count()

    paginator = Paginator(favs, 40)
    page = request.GET.get('page')
    favs = paginator.get_page(page)

    context = {'favs': favs,
               'favs_count': favs_count
               }
    return render(request, 'dashboard/fav.html', context)


# class NotesDetailView(LoginRequiredMixin, generic.DetailView):
#     model = Notes

@login_required
def NotesDetailView(request, code_id):
    notes = get_object_or_404(Notes, pk=code_id)
    print('notes', notes)
    if request.method == "POST":
        if notes.fav == True:
            notes.fav = False
            notes.save()
        else:
            notes.fav = True
            notes.save()
        return redirect('notes_detail', notes.pk)
    context = {'notes': notes}
    return render(request, 'dashboard/notes_detail.html', context)


@login_required
def create_note(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, language=request.POST['language'], code_here=form.cleaned_data['code_here'], notes_for_yourself=request.POST['notes_for_yourself'],)
            notes.save()
            messages.success(
                request, f"{request.user.username.upper()} **{request.POST['language']}** Code  Added  Succcessfully!!!")
            return redirect("notes")
    else:
        form = NotesForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/form.html', context)


@login_required
def update_note(request, pk):
    page = 'update'
    obj = Notes.objects.get(id=pk)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"{request.user.username.upper()} **{obj}** Code has been Updated Succcessfully!!!")
            return redirect("notes_detail", obj.id)
        # return HttpResponseRedirect(request.path_info)
    else:
        form = NotesForm(instance=obj)
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes,
               'form': form,
               'page': page,
               }
    return render(request, 'dashboard/form.html', context)


@login_required
def delete_note(request, pk=None):
    note = Notes.objects.get(id=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(
            request, f" {request.user.username.upper()} **{note}** Code has been deleted Succcessfully!!!")
        return redirect("notes")

    context = {'obj': note,
               }
    return render(request, 'dashboard/delete.html', context)


@login_required
def homework(request):
    page = 'create'
    homeworks = Homework.objects.filter(user=request.user, is_finished=False)
    homeworks_completed = Homework.objects.filter(
        user=request.user, is_finished=True)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False

    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(
                user=request.user,
                customer=request.POST['customer'],
                assembly=request.POST['assembly'],
                qty=request.POST['qty'],
                comments=form.cleaned_data['comments'],
                due=request.POST['due'],
                is_finished=finished
            )
            homework.save()
            messages.success(
                request, f"{request.user.username.upper()} Assembly Added Succcessfully!!!")
            return redirect('home-work')
    else:
        form = HomeworkForm()
    context = {'homeworks': homeworks,
               'homework_done': homework_done,
               'form': form,
               'page': page,
               'homeworks_completed': homeworks_completed
               }
    return render(request, 'dashboard/homework.html', context)


@login_required
def create_assembly(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(
                user=request.user,
                customer=request.POST['customer'],
                assembly=request.POST['assembly'],
                qty=request.POST['qty'],
                comments=form.cleaned_data['comments'],
                due=request.POST['due'],
                is_finished=finished
            )
            homework.save()
            messages.success(
                request, f"Assembly Added from {request.user.username.upper()} Succcessfully!!!")
            return redirect('home-work')
    else:
        form = HomeworkForm()
    context = {
        'form': form,

    }
    return render(request, 'dashboard/form.html', context)


@login_required
def update_homework(request, pk=None):
    page = "update"
    homework = Homework.objects.get(id=pk)
    if request.method == 'POST':
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            homework.save()
            messages.success(
                request, f"{request.user.username.upper()} Assembly has beed updated Succcessfully!!!")
            return redirect('home-work')
    else:
        form = HomeworkForm(instance=homework)
    context = {
        'form': form,
        'page': page
    }
    return render(request, 'dashboard/form.html', context)


@login_required
def complete_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    messages.success(
        request, f"{request.user.username.upper()} Assembly has beed completed Succcessfully!!!")
    return redirect("home-work")


@login_required
def delete_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if request.method == 'POST':
        homework.delete()
        messages.success(
            request, f"{request.user.username.upper()} Assembly has beed deleted Succcessfully!!!")
        return redirect("home-work")
    context = {'obj': homework,
               }
    return render(request, 'dashboard/delete.html', context)


@login_required
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],

            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['descripiton'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/youtube.html', context)

    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/youtube.html', context)


@login_required
def todo(request):
    todos = Todo.objects.filter(user=request.user).order_by('-pk')
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todo.save()
            messages.success(
                request, f"Todo Added from {request.user.username.upper()} Succcessfully!!!")
            return redirect('todo')
    else:
        form = TodoForm()
    context = {
        'todos': todos,
        'todos_done':   todos_done,
        'form': form
    }
    return render(request, 'dashboard/todo.html', context)


@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    messages.success(
        request, f"{request.user.username.upper()} Todo ({todo.title}) has beed updated Succcessfully!!!")
    return redirect("todo")


@login_required
def delete_todo(request, pk=None):
    todo = Todo.objects.get(id=pk).delete()
    messages.success(
        request, f"{request.user.username.upper()} Todo has beed deleted Succcessfully!!!")
    return redirect("todo")


def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),

            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html', context)

    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ''

            }
        return render(request, 'dashboard/dictionary.html', context)

    form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == "POST":
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            "form": form,
            'title': search.title,
            "link": search.url,
            "details": search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/wiki.html', context)


def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and (int(float(input))) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {float(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {float(input)/3} yard'

                    if first == 'meter' and second == 'foot':
                        answer = f'{input} meter = {float(input)*3.28084} foot'
                    if first == 'foot' and second == 'meter':
                        answer = f'{input} meter = {float(input)/3.28084} foot'

                    if first == 'meter' and second == 'inch':
                        answer = f'{input} meter = {float(input)*39.3701} inch'
                    if first == 'inch' and second == 'meter':
                        answer = f'{input} meter = {float(input)/39.3701} inch'

                    context = {
                        'form': form,
                        'm_form': measurement_form,
                        'input': True,
                        'answer': answer
                    }

        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound= {int(input)*0.453592} Kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                    context = {
                        'form': form,
                        'm_form': measurement_form,
                        'input': True,
                        'answer': answer
                    }

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.capitalize()
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"{username.upper()}  Account has been created!!!")
            return redirect('login')
        else:
            messages.error(request, f"Some thing went wrong. pls try again")
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }

    return render(request, 'dashboard/register.html', context)


@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False

    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done

    }
    return render(request, 'dashboard/profile.html', context)
