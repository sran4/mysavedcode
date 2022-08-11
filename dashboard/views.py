
from django.contrib.auth.mixins import LoginRequiredMixin
from django import contrib
from django.core.checks import messages
from django.forms.widgets import FileInput
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Notes, Homework, Category
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.template.loader import render_to_string

from django.contrib.auth.models import Group, User


def home(request):
    return render(request, 'home.html')


def handle404(request, exception):
    return render(request, '404.html', )


def handle500(request):
    return render(request, '404.html', )


@login_required
def notes(request, c_slug=None):
    c_page = None
    notes = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        q = c_page
        notes = Notes.objects.filter(user=request.user, category=c_page)

    else:
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        notes = Notes.objects.filter(user=request.user).filter(
            Q(language__icontains=q) |
            Q(notes_for_yourself__icontains=q)).order_by('-updated_at')

    favNotes_count = Notes.objects.filter(
        user=request.user, fav=True).count()
    notes_count = notes.count()
    paginator = Paginator(notes, 96)
    page = request.GET.get('page')
    notes = paginator.get_page(page)
    context = {'notes': notes,
               'Q': q,
               'notes_count': notes_count,
               'favNotes_count': favNotes_count,
               }
    return render(request, 'dashboard/notes/notes.html', context)


@login_required
def favs_notes(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    allNotes_count = Notes.objects.filter(user=request.user).count()
    favs = Notes.objects.filter(user=request.user, fav=True).filter(
        Q(language__icontains=q) |
        Q(notes_for_yourself__icontains=q) |
        Q(code_here__icontains=q)).order_by('-updated_at')

    favs_count = favs.count()

    paginator = Paginator(favs, 80)
    page = request.GET.get('page')
    favs = paginator.get_page(page)

    context = {'favs': favs,
               'favs_count': favs_count,
               'allNotes_count': allNotes_count
               }
    return render(request, 'dashboard/notes/fav.html', context)


@login_required
def top_notes(request):
    top_page = 'top'
    allNotes_count = Notes.objects.filter(user=request.user).count()
    top = Notes.objects.filter(user=request.user, top=True)
    top_count = top.count()
    paginator = Paginator(top, 80)
    page = request.GET.get('page')
    top = paginator.get_page(page)

    context = {'favs': top,
               'favs_count': top_count,
               'allNotes_count': allNotes_count,
               'page': top_page,
               }
    return render(request, 'dashboard/notes/fav.html', context)


@login_required
def tag_notes(request, slug=None):

    allNotes_count = Notes.objects.filter(user=request.user).count()

    tags_Notes = None
    if slug != None:
        tags_Notes = Notes.objects.filter(user=request.user, tags__slug=slug)
    else:
        tags_Notes = Notes.objects.filter(user=request.user)
    tags = Tag.objects.all()

    top_count = tags_Notes.count()
    paginator = Paginator(tags_Notes, 80)
    page = request.GET.get('page')
    tags_Notes = paginator.get_page(page)

    context = {'favs': tags_Notes,
               'tags': tags,
               'favs_count': top_count,
               'allNotes_count': allNotes_count,

               }
    return render(request, 'dashboard/notes/tags.html', context)


# class NotesDetailView(LoginRequiredMixin, generic.DetailView):
#     model = Notes

    # __icontains = field contains this
    # __iexact = fields is exactly this
    # '''

# for favs notes details
def NotesDetailView(request,  note_slug):
    try:
        note = Notes.objects.get(slug=note_slug)
    except Exception as e:
        raise e

    if request.method == "POST" and request.is_ajax():
        if note.fav == True:
            note.fav = False
            note.save()
        else:
            note.fav = True
            note.save()
        return redirect('notes_detail', note.slug)
    context = {'note': note}
    if request.is_ajax():
        html = render_to_string('dashboard/notes/fav_section.html',
                                context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'dashboard/notes/notes_detail.html', context)


# for Top Top page notes details
def NotesDetailView1(request,  note_slug):
    try:
        note = Notes.objects.get(slug=note_slug)
    except Exception as e:
        raise e

    if request.method == "POST" and request.is_ajax():
        if note.top == True:
            note.top = False
            note.save()
        else:
            note.top = True
            note.save()
        return redirect('notes_detail1', note.slug)
    context = {'note': note}
    if request.is_ajax():
        html = render_to_string('dashboard/notes/top_section.html',
                                context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'dashboard/notes/notes_detail.html', context)


# def NotesDetailView(request,  note_slug):
#     try:
#         note = Notes.objects.get(slug=note_slug)
#     except Exception as e:
#         raise e

#     if request.method == "POST" and request.is_ajax():
#         if note.fav == True:
#             note.fav = False
#             note.save()
#         else:
#             note.fav = True
#             note.save()
#         return redirect('notes_detail', note.slug)
#     context = {'note': note}
#     if request.is_ajax():
#         html = render_to_string('dashboard/notes/fav_section.html',
#                                 context, request=request)
#         return JsonResponse({'form': html})
#     return render(request, 'dashboard/notes/notes_detail.html', context)


# @login_required
# def NotesDetailViewT(request, code_id):
#     note = get_object_or_404(Notes, pk=code_id)
#     print('note', note)
#     if request.method == "POST":
#         if note.fav == True:
#             note.fav = False
#             note.save()
#         else:
#             note.fav = True
#             note.save()
#         return redirect('notes_detail', note.pk)
#     context = {'note': note}
#     return render(request, 'dashboard/notes/notes_detail.html', context)


@login_required
def create_note(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        data = request.POST
        category = Category.objects.get(id=data['category'])
        if form.is_valid():
            note = Notes(
                user=request.user,
                language=request.POST['language'],
                code_here=form.cleaned_data['code_here'],
                notes_for_yourself=request.POST['notes_for_yourself'],
                fav=form.cleaned_data['fav'],
                top=form.cleaned_data['top'],
                category=category,
            )
            note.save()
            note = Notes.objects.get(id=note.id)
            tags = form.cleaned_data['tags']
            print(tags)
            note.tags.add(*tags)
            messages.success(
                request, f"{request.user.username.upper()} **{request.POST['language']}** Code  Added  Succcessfully!!!")
            return redirect('notes_detail', note.slug)

    else:
        form = NotesForm()
    context = {
        'form': form,
    }
    return render(request, 'form.html', context)


# @login_required
# def create_note(request):
#     if request.method == 'POST':
#         data = request.POST
#         category = Category.objects.get(id=data['category'])
#         form = NotesForm(request.POST)
#         if form.is_valid():
#             notes = Notes(
#                 user=request.user,
#                 language=request.POST['language'],
#                 code_here=form.cleaned_data['code_here'],
#                 notes_for_yourself=request.POST['notes_for_yourself'],
#                 fav=form.cleaned_data['fav'],
#                 top=form.cleaned_data['top'],
#                 category=category,
#             )

#             notes.save()
#             messages.success(
#                 request, f"{request.user.username.upper()} **{request.POST['language']}** Code  Added  Succcessfully!!!")
#             return redirect("notes")
#     else:
#         form = NotesForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'form.html', context)


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
            return redirect("notes_detail", obj.slug)
        # return HttpResponseRedirect(request.path_info)
    else:
        form = NotesForm(instance=obj)
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes,
               'form': form,
               'page': page,
               }
    return render(request, 'form.html', context)


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
    return render(request, 'delete.html', context)


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
    return render(request, 'dashboard/misc/homework.html', context)


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
    return render(request, 'form.html', context)


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
    return render(request, 'form.html', context)


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
    return render(request, 'delete.html', context)


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
        return render(request, 'dashboard/misc/youtube.html', context)

    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/misc/youtube.html', context)


@login_required
def todo(request):
    todos = Todo.objects.filter(
        user=request.user, is_finished=False).order_by('-pk')
    todos_completed = Todo.objects.filter(
        user=request.user, is_finished=True).order_by('-pk')
    print(todos)
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
        'todos_completed': todos_completed,
        'form': form
    }
    return render(request, 'dashboard/misc/todo.html', context)


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
        return render(request, 'dashboard/misc/books.html', context)

    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/misc/books.html', context)


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
        return render(request, 'dashboard/misc/dictionary.html', context)

    form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/misc/dictionary.html', context)


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
        return render(request, 'dashboard/misc/wiki.html', context)
    form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/misc/wiki.html', context)


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
    return render(request, 'dashboard/misc/conversion.html', context)


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
    return render(request, 'dashboard/misc/profile.html', context)


def generatePassword(request):
    return render(request, 'dashboard/misc/password.html')


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.capitalize()
            form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Customer')
            user.groups.add(group)
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

    return render(request, 'dashboard/auth/register.html', context)
