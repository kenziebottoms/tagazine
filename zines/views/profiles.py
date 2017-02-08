from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.messages import constants as message_constants

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