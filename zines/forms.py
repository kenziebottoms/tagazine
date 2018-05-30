from django import forms
from django.forms import ModelForm
from .models import *
from django.shortcuts import get_object_or_404
from .widgets import *

class ZineForm(ModelForm):
    class Meta:
        model = Zine
        fields = [
            'title',
            'tagline',
            'show_author',
            'external',
            'submissions_open',
            'start_date',
            'end_date',
            'desc',
            'contact_email',
            'submission_email',
            'website',
            'cover',
            'primary_language',
            'locale',
            'published'
        ]
        widgets = {
            'title' : forms.TextInput(attrs={
                'class' : 'heading',
                'placeholder' : 'Title'
            }),
            'desc' : forms.HiddenInput,
            'published' : forms.HiddenInput,
            'start_date' : HTML5DateInput,
            'end_date' : HTML5DateInput,
        }
        labels = {
            'title' : '',
        }

    tags = forms.CharField(widget=forms.HiddenInput,required=False)

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['tags'] = [t.pk for t in kwargs['instance'].tags.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        def save_tags():
            instance.tags.clear()
            # TODO: regex
            tag_data = self.cleaned_data['tags'].replace('[', '');
            if tag_data != '':
                tag_data = tag_data.replace('[', '');
                tag_data = tag_data.split(',');
                for tag in tag_data:
                    instance.tags.add(tag)
        if commit:
            instance.save()
            save_tags()

        return instance

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = [
            'title',
            'desc',
            'pub_date',
            'published',
            'cover',
            'guest_authors',
            'ext_guest_authors'
        ]
        widgets = {
            'pub_date' : HTML5DateInput,
            'desc' : forms.HiddenInput,
            'published' : forms.HiddenInput,
            'ext_guest_authors' : forms.Textarea(attrs={
                'placeholder' : 'Ruth Bader Ginsburg, Viggo Mortenson, Axl Rose',
                'rows' : '4',
            })
        }
    def save(self, commit=True):
        issue = super(IssueForm, self).save(commit)
        issue.create_thumb()
        return issue

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'bio',
            'website',
            'contact_email',
            'pic',
            'location'
        ]
        widgets = {
            'bio' : forms.HiddenInput,
        }

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=True)
        profile.create_thumb()
        return profile
