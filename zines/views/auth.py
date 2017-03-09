from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.messages import constants as message_constants

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
    return render(request, 'zines/login.html', context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')