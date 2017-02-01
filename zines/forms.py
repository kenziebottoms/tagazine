from django import forms
from django.forms import ModelForm
from .models import Zine
from django.shortcuts import get_object_or_404

class ZineForm(ModelForm):
    class Meta:
        model = Zine
        fields = ['title', 'start_date', 'end_date', 'authors', 'show_author', 'external', 'submissions_open', 'desc', 'contact_email', 'submission_email', 'tagline', 'website', 'cover', 'locale']
        widgets = {
            'title' : forms.TextInput(attrs={
                'class':'heading',
                'placeholder':'Title'
            }),
            'desc' : forms.HiddenInput,
            'start_date' : forms.SelectDateWidget,
            'end_date' : forms.SelectDateWidget,
        }
        labels = {
            'title' : '',
        }