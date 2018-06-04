from django.shortcuts import render

from user.forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
    else:
        return render(request, 'register.html', {})


def login(request):
    return render(request, 'login.html', {})


def user_info(request):
    return render(request, 'user_info.html', {})


def logout(request):
    return render(request, 'logout.html', {})
