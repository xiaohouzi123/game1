from django.shortcuts import render


def create(request):
    return render(request, 'create.html', {})


def edit(request):
    return render(request, 'edit.html', {})


def read(request):
    return render(request, 'read.html', {})


def post_list(request):
    return render(request, 'post_list.html', {})


def search(request):
    return render(request, 'search.html', {})
