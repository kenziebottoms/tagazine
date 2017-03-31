from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

import zines, profiles, issues, api, auth

def index(request):
    recent_issues = Issue.objects.filter(published=True).order_by('-pub_date')[:3]
    new_users = Profile.objects.order_by('member_since')[:5]
    recent_zines = Zine.objects.filter(published=True).all();
    recent_zines = sorted(recent_zines, key=lambda i: i.lastUpdated())[:3]
    recent_zines.reverse()
    tag_ids = []
    for zine in recent_zines:
        tag_ids += zine.tags.values_list('id',flat=True)
    recent_tags = Tag.objects.filter(pk__in=tag_ids)
    context = {
        'recent_issues' : recent_issues,
        'new_users' : new_users,
        'recent_zines' : recent_zines,
        'recent_tags' : recent_tags,
    }
    return render(request, 'zines/index.html', context)

def drafts(request):
    user = request.user
    profile = user.profile
    private_zines = Zine.objects.filter(authors=profile,published=False)
    private_issues = Issue.objects.filter(zine__authors=profile,published=False)
    context = {
        'profile' : profile,
        'zines' : private_zines,
        'issues' : private_issues,
        'messages' : messages.get_messages(request),
    }
    return render(request, 'zines/drafts.html', context)

def tag(request, slug):
    tag = Tag.objects.filter(slug=slug).first()
    zines = Zine.objects.filter(tags__slug=slug)
    context = {
        'zines' : zines,
        'tag' : tag,
    }
    return render(request, 'zines/tag.html', context)

def search(request):
    term = request.GET['term']
    zines = Zine.objects.filter(title__icontains=term) | Zine.objects.filter(desc__icontains=term) | Zine.objects.filter(tagline__icontains=term)
    issues = Issue.objects.filter(title__icontains=term) | Issue.objects.filter(desc__icontains=term) | Issue.objects.filter(ext_guest_authors__icontains=term)
    profiles = Profile.objects.filter(user__username__icontains=term) | Profile.objects.filter(name__icontains=term) | Profile.objects.filter(bio__icontains=term)
    tags = Tag.objects.filter(slug__icontains=term) | Tag.objects.filter(title__icontains=term)
    context = {
        'zines' : zines[:20],
        'issues' : issues[:20],
        'profiles' : profiles[:20],
        'tags' : tags[:20],
        'term' : term,
    }
    return render(request, 'zines/search.html', context)

def dash(request):
    user_id = request.user.id
    profile = get_object_or_404(Profile, pk=request.user.profile.id)
    context = {
        'profile' : profile
    }
    return render(request, 'zines/dash.html', context)
