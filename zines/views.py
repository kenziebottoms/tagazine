from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *

def index(request):
    recent_issues = Issue.objects.order_by('-pub_date')[:3]
    new_users = Profile.objects.order_by('member_since')[:5]
    context = {
        'recent_issues' : recent_issues,
        'new_users' : new_users,
    }
    return render(request, 'zines/index.html', context)

def profile(request, profile_id):
    profile = get_object_or_404(Profile,pk=profile_id)
    works = Authorship.objects.filter(user_profile=profile_id,hideIdentity=False)
    works = sorted(works, key=lambda i: i.zine.lastUpdated())
    works.reverse()
    guest_works = Issue.objects.filter(guest_authors=profile_id).order_by('pub_date')
    context = {
        'profile' : profile,
        'works' : works,
        'guest_works' : guest_works,
    }
    return render(request, 'zines/profile.html', context)

def zine(request, zine_id):
    zine = get_object_or_404(Zine,pk=zine_id)
    issues = Issue.objects.filter(zine=zine_id)
    authorships = Authorship.objects.filter(zine=zine_id)
    context = {
        'zine' : zine,
        'issues' : issues,
        'authorships' : authorships,
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
    }
    if request.method == "POST":
        form = ZineForm(request.POST,instance=zine)
        if form.is_valid():
            context['response'] = 1
            zine = form.save()
            context['zine'] = zine
        else:
            context['response'] = 0
            context['error'] = 'Invalid input'
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
    }
    return render(request, 'zines/issue.html', context)
