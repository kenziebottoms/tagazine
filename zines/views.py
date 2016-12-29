from django.shortcuts import render, get_object_or_404
from .models import *

def user(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    works = Authorship.objects.filter(user=user_id)
    context = {
        'user' : user,
        'works' : works
    }
    return render(request, 'zines/user.html', context)

def zine(request, zine_id):
    zine = get_object_or_404(Zine,pk=zine_id)
    context = {
        'zine', zine,
    }
    return render(request, 'zines/zine.html', context)