from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

import zines, profiles, issues, api

def index(request):
    recent_issues = Issue.objects.filter(published=True).order_by('-pub_date')[:3]
    new_users = Profile.objects.order_by('member_since')[:5]
    recent_zines = Zine.objects.filter(published=True).all();
    recent_zines = sorted(recent_zines, key=lambda i: i.lastUpdated())[:5]
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
    user_id = request.user.id
    profile = Profile.objects.filter(user=user_id)[0]
    unpub_authorships = Authorship.objects.filter(user_profile=profile.id,zine__published=False)
    works = Authorship.objects.filter(user_profile=profile.id)
    issue_ids = []
    for work in works:
        new_ids = work.zine.unPublishedContent().values_list('id',flat=True)
        if new_ids:
            issue_ids += list(new_ids)
    issues = Issue.objects.filter(pk__in=issue_ids)
    context = {
        'profile' : profile,
        'works' : unpub_authorships,
        'issues' : issues,
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
