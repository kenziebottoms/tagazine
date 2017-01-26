from django import forms
from django.forms import ModelForm
from .models import Zine
from django.shortcuts import get_object_or_404

class ZineForm(ModelForm):
    class Meta:
        model = Zine
        fields = ['title', 'authors', 'show_author', 'external', 'submissions_open']