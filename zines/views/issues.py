from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

def issue(request, zine_id, issue_no):
    issue = Issue.objects.filter(zine=zine_id,number=issue_no)[0]
    pages = Page.objects.filter(issue=issue.id)
    context = {
        'issue' : issue,
        'pages' : pages,
        'messages' : messages.get_messages(request),
    }
    return render(request, 'zines/issue.html', context)