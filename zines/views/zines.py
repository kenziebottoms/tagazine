from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

def zine(request, zine_id=0, slug=''):
    context = {}
    if zine_id:
        zine = get_object_or_404(Zine,pk=zine_id)
    else:
        if Zine.objects.filter(slug=slug).exists():
            zine = Zine.objects.get(slug=slug)
        else:
            return redirect('index')
    authors = zine.authors.all()
    if request.user.id in map(lambda a: a.user.id, authors):
        issues = Issue.objects.filter(zine=zine.id)
    else:
        issues = Issue.objects.filter(zine=zine.id,published=True)
    tags = zine.tags.all()
    context = {
        'zine' : zine,
        'issues' : issues,
        'authors' : authors,
        'messages' : messages.get_messages(request),
        'tags' : tags,
    }
    return render(request, 'zines/zine.html', context)

def edit_zine(request, zine_id=0, slug=''):
    if zine_id:
        zine = get_object_or_404(Zine,pk=zine_id)
        return redirect('zine', zine.slug)
    else:
        zine = Zine.objects.get(slug=slug)
        zine_id = zine.id
    issues = Issue.objects.filter(zine=zine.id)
    authors = zine.authors.all()
    context = {
        'zine' : zine,
        'issues' : issues,
        'authors' : authors,
        'messages' : messages.get_messages(request),
    }
    if request.method == "POST":
        form = ZineForm(request.POST,request.FILES,instance=zine)
        if form.is_valid():
            zine = form.save()
            messages.add_message(request, message_constants.SUCCESS, 'Your changes were saved.', 'check')
            return redirect('zine', zine_id)
        else:
            messages.add_message(request, message_constants.ERROR, 'Your changes were not saved.', 'close')
            context['form'] = form
    else:
        form = ZineForm(instance=zine)
        context['form'] = form
    return render(request, 'zines/backend/edit-zine.html', context)

def new_zine(request):
    context = {}
    if request.method == "POST":
        form = ZineForm(request.POST,request.FILES)
        if form.is_valid():
            zine = form.save()
            zine.authors = {request.user.profile}
            zine.owner = request.user.profile
            zine.save()
            messages.add_message(request, message_constants.SUCCESS, 'Your changes were saved.', 'check')
            return redirect('zine', zine.id)
        else:
            messages.add_message(request, message_constants.ERROR, form.errors, 'close')
            context['form'] = form
    else:
        form = ZineForm(initial={'desc':''})
        context['form'] = form
    context['messages'] = messages.get_messages(request)
    return render(request, 'zines/backend/edit-zine.html', context)