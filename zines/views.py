from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

def index(request):
    recent_issues = Issue.objects.filter(published=True).order_by('-pub_date')[:3]
    new_users = Profile.objects.order_by('member_since')[:5]
    recent_zines = Zine.objects.filter(published=True).all();
    recent_zines = sorted(recent_zines, key=lambda i: i.lastUpdated())[:5]
    recent_zines.reverse()
    context = {
        'recent_issues' : recent_issues,
        'new_users' : new_users,
        'recent_zines' : recent_zines,
    }
    return render(request, 'zines/index.html', context)

def profile(request, profile_id):
    profile = get_object_or_404(Profile,pk=profile_id)
    works = Authorship.objects.filter(user_profile=profile_id,hideIdentity=False,zine__published=True)
    works = sorted(works, key=lambda i: i.zine.lastUpdated())
    works.reverse()
    guest_works = Issue.objects.filter(guest_authors=profile_id,published=True).order_by('pub_date')
    context = {
        'profile' : profile,
        'works' : works,
        'guest_works' : guest_works,
        'messages' : messages.get_messages(request),
    }
    return render(request, 'zines/profile.html', context)

def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile,pk=profile_id)
    context = {
        'profile' : profile,
        'messages' : messages.get_messages(request),
    }
    if request.method == "POST":
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.add_message(request, message_constants.SUCCESS, 'Your profile was saved.', 'check')
            return redirect('profile', profile.id)
        else:
            context['response'] = 0
            context['error'] = 'Invalid input'
            context['form'] = form
    else:
        form = ProfileForm(instance=profile)
        context['form'] = form
    return render(request, 'zines/edit-profile.html', context)

def zine(request, zine_id):
    zine = get_object_or_404(Zine,pk=zine_id)
    issues = Issue.objects.filter(zine=zine_id,published=True)
    authorships = Authorship.objects.filter(zine=zine_id)
    context = {
        'zine' : zine,
        'issues' : issues,
        'authorships' : authorships,
        'messages' : messages.get_messages(request),
    }
    return render(request, 'zines/zine.html', context)

def edit_zine(request, zine_id):
    zine = get_object_or_404(Zine,pk=zine_id)
    issues = Issue.objects.filter(zine=zine_id)
    authorships = Authorship.objects.filter(zine=zine_id)
    context = {
        'zine' : zine,
        'issues' : issues,
        'authorships' : authorships,
        'messages' : messages.get_messages(request),
    }
    if request.method == "POST":
        form = ZineForm(request.POST,instance=zine)
        if form.is_valid():
            zine = form.save()
            messages.add_message(request, message_constants.SUCCESS, 'Your changes were saved.', 'check')
            return redirect('zine', zine.id)
        else:
            context['response'] = 0
            context['error'] = 'Invalid input'
            context['form'] = form
    else:
        form = ZineForm(instance=zine)
        context['form'] = form
    return render(request, 'zines/edit-zine.html', context)

def issue(request, zine_id, issue_no):
    issue = Issue.objects.filter(zine=zine_id,number=issue_no)[0]
    pages = Page.objects.filter(issue=issue.id)
    context = {
        'issue' : issue,
        'pages' : pages,
        'messages' : messages.get_messages(request),
    }
    return render(request, 'zines/issue.html', context)

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