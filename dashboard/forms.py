from django import forms
from django.forms import widgets
from . models import *
from ckeditor.fields import RichTextFormField

from django.contrib.auth.forms import UserCreationForm
from django.forms import CheckboxInput, ModelChoiceField, Select, ModelMultipleChoiceField, SelectMultiple


class NotesForm(forms.ModelForm):
    notes_for_yourself = forms.CharField(label="Notes to search", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Add a keywords to search for this note!', 'rows': '2', 'cols': '150'}))

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(
    ), widget=forms.CheckboxSelectMultiple, required=False, label="TAGS_If wants to tag,  Press 'Ctrl' to select multiple tags")

    class Meta:
        model = Notes

        labels = {
            "language": "Title",
            "code_here": "Better with Copy and Paste Raw Data from Github",
            "fav": "Check if wants to add in your Favourite code Pages",
            "top": "Check if wants to add in your Main code pages",

        }

        fields = ['language', 'category', 'notes_for_yourself',
                  'code_here', 'tags', 'fav', 'top', ]
        exclude = ('slug', 'user')

    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Please choose Category"


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
