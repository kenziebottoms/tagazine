from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
    recent_issues = Issue.objects.order_by('pub_date')[:5]
    new_users = Profile.objects.order_by('member_since')[:5]
    context = {
        'recent_issues' : recent_issues,
        'new_users' : new_users,
    }
    return render(request, 'zines/index.html', context)

def profile(request, profile_id):
    profile = get_object_or_404(Profile,pk=profile_id)
    works = Authorship.objects.filter(user_profile=profile_id,hideIdentity=False)
    guest_works = Issue.objects.filter(guest_authors=profile_id)
    context = {
        'user' : profile,
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

def issue(request, zine_id, issue_no):
    issue = Issue.objects.filter(zine=zine_id,number=issue_no)[0]
    context = {
        'issue' : issue,
    }
    return render(request, 'zines/issue.html', context)
