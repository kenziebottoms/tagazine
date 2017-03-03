from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

def issue(request, zine_id, issue_no):
    issue = Issue.objects.filter(zine=zine_id,number=issue_no).first()
    pages = Page.objects.filter(issue=issue.id)
    authorships = Authorship.objects.filter(zine=zine_id)
    context = {
        'issue' : issue,
        'pages' : pages,
        'authorships' : authorships,
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
        if request.FILES:
            form = IssueForm(request.POST,request.FILES,instance=issue)
        else:
            form = IssueForm(request.POST,instance=issue)
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
    return render(request, 'zines/edit-issue.html', context)