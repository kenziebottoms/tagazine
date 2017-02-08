from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

def zine(request, zine_id):
    zine = get_object_or_404(Zine,pk=zine_id)
    issues = Issue.objects.filter(zine=zine_id,published=True)
    authorships = Authorship.objects.filter(zine=zine_id)
    tags = zine.tags.all()
    context = {
        'zine' : zine,
        'issues' : issues,
        'authorships' : authorships,
        'messages' : messages.get_messages(request),
        'tags' : tags,
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