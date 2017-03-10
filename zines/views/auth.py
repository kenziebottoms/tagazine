from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.messages import constants as message_constants
from django.contrib.auth.models import User

def login_view(request):
    context = []
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, message_constants.ERROR, 'Invalid username and/or password.', 'close')
    return render(request, 'zines/auth/login.html', context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def signup(request):
    context = {}
    if request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        context['username'] = username
        context['email'] = email
        if User.objects.filter(username=username):
            messages.add_message(request, message_constants.ERROR, 'That username is taken.', 'close')
        elif User.objects.filter(email=email):
            messages.add_message(request, message_constants.ERROR, 'That email is already associated with an account.', 'close')
        elif password != password2:
            messages.add_message(request, message_constants.ERROR, 'Your passwords do not match.', 'close')
        else:
            user = User.objects.create_user(username, email, password)
            user.save()
            user = authenticate(username=username,password=password)
            login(request, user)
            return redirect('index')
    return render(request, 'zines/auth/signup.html', context)
