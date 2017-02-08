from django import forms
from django.forms import ModelForm
from .models import Zine, Profile, Issue
from django.shortcuts import get_object_or_404
import html5.forms.widgets as html5_widgets

class ZineForm(ModelForm):
    class Meta:
        model = Zine
        fields = ['title', 'tagline', 'authors', 'show_author', 'external', 'submissions_open', 'start_date', 'end_date', 'desc', 'contact_email', 'submission_email', 'website', 'cover', 'locale', 'published']
        widgets = {
            'title' : forms.TextInput(attrs={
                'class' : 'heading',
                'placeholder' : 'Title'
            }),
            'desc' : forms.HiddenInput,
            'published' : forms.HiddenInput,
            'start_date' : html5_widgets.DateInput,
            'end_date' : html5_widgets.DateInput,
        }
        labels = {
            'title' : '',
        }
        css_class = {
            'show_author' : 'large-4 medium-4 small-12 columns'
        }

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'desc', 'pub_date', 'published', 'cover', 'guest_authors', 'ext_guest_authors']
        widgets = {
            'title' : forms.TextInput(attrs={
                'class' : 'heading',
            }),
            'pub_date' : html5_widgets.DateInput,
            'desc' : forms.HiddenInput,
            'published' : forms.HiddenInput,
            'ext_guest_authors' : forms.Textarea(attrs={
                'placeholder' : 'Ruth Bader Ginsburg, Viggo Mortenson, Axl Rose',
                'rows' : '4',
            })
        }
        labels = {
            'title' : '',
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'website', 'contact_email', 'pic', 'location']
        widgets = {
            'bio' : forms.HiddenInput,
        }