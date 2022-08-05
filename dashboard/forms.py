from django import forms
from django.forms import widgets
from . models import *
from ckeditor.fields import RichTextFormField

from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        labels = {
            "language": "Type Language of code",
            "notes_for_yourself": "Notes for yourself and for search",
            "code_here": "Copy and Paste Raw Data from Github",
            "fav": "Mark it if wants to add in your Favourite code",
            "top": "Mark it if wants to add in your Main code"
        }

        # widgets = {
        #     'code_here': RichTextFormField(),

        # }
        fields = ['language', 'category', 'notes_for_yourself',
                  'code_here', 'fav', 'top',]
# widgets may not need it here


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()

                   }
        fields = ['customer', 'assembly', 'qty',
                  'comments', 'due', 'is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label='Type your search:')


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']


class ConversionForm(forms.Form):
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class ConversionLengthForm(forms.Form):
    CHOICES = [('inch', 'inch'), ('foot', 'foot'),
               ('meter', 'meter'), ('yard', 'yard')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'step': 'any',
               'placeholder': 'Enter the number'}
    ))

    measure1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

    measure2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )


class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'pound'), ('kilogram', 'kilogram')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number',
               'placeholder': 'Enter the number'}
    ))

    measure1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

    measure2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
