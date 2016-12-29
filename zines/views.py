from django.shortcuts import render, get_object_or_404
from .models import *

def user(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    works = Authorship.objects.filter(user=user_id,hideIdentity=False)
    context = {
        'user' : user,
        'works' : works
    }
    return render(request, 'zines/user.html', context)

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

def index(request):
    recent_issues = Issue.objects.order_by('pub_date')[:5]
    context = {
        'recent_issues' : recent_issues,
    }
    return render(request, 'zines/index.html', context)