from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

def issue(request, zine_id, issue_no):
    issue = Issue.objects.filter(zine=zine_id,number=issue_no).first()
    pages = Page.objects.filter(issue=issue.id)
    zine = get_object_or_404(Zine, pk=zine_id)
    authors = zine.authors.all()
    context = {
        'issue' : issue,
        'pages' : pages,
        'authors' : authors,
        'messages' : messages.get_messages(request),
    }
    return render(request, 'zines/issue.html', context)

def edit_issue(request, zine_id, issue_no):
    issue = Issue.objects.filter(zine=zine_id,number=issue_no).first()
    pages = Page.objects.filter(issue=issue.id)
    context = {
        'issue' : issue,
        'pages' : pages,
        'messages' : messages.get_messages(request),
    }
    if request.method == "POST":
        form = IssueForm(request.POST,request.FILES,instance=issue)
        if form.is_valid():
            issue = form.save()
            messages.add_message(request, message_constants.SUCCESS, 'Your changes were saved.', 'check')
            return redirect('issue', issue.zine.id, issue.number)
        else:
            messages.add_message(request, message_constants.ERROR, 'Your changes were not saved.', 'close')
            context['form'] = form
    else:
        form = IssueForm(instance=issue)
        context['form'] = form
    return render(request, 'zines/backend/edit-issue.html', context)

def new_issue(request, zine_id):
    context = {}
    zine = get_object_or_404(Zine, pk=zine_id)
    if request.method == "POST":
        form = IssueForm(request.POST,request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.zine = zine
            issue.save()
            messages.add_message(request, message_constants.SUCCESS, 'Your changes were saved.', 'check')
            return redirect('issue', zine.id, issue.number)
        else:
            messages.add_message(request, message_constants.ERROR, form.errors, 'close')
            context['form'] = form
    else:
        form = IssueForm(initial={'desc':'', 'pub_date':datetime.datetime.now})
        context['form'] = form
    context['messages'] = messages.get_messages(request)
    return render(request, 'zines/backend/edit-issue.html', context)