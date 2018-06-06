from math import ceil

from django.shortcuts import render, redirect
from django.core.cache import cache

from post.models import Post


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%d' % post.id)
    else:
        return render(request, 'create.html')


def edit(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)

        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        cache.set('Post-%s' % post_id, post)  # 修改缓存，使缓存与数据库保持一致
        return redirect('/post/read/?post_id=%d' % post.id)
    else:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(id=post_id)
        return render(request, 'edit.html', {'post': post})


def read(request):
    post_id = int(request.GET.get('post_id'))
    try:
        key = 'Post-%s' % post_id
        post = cache.get(key)  # 先从缓存获取元素
        print('get from cache', post_id)
        if post is None:
            post = Post.objects.get(id=post_id)  # 取不到的时候，从数据库获取
            cache.set(key, post)                 # 将取到的结果存入缓存，以便后续获取
            print('get from db', post_id)
        return render(request, 'read.html', {'post': post})
    except Post.DoesNotExist:
        return redirect('/')


def post_list(request):
    page = int(request.GET.get('page', 1))  # 当前页码，默认为 1

    per_page = 5
    # 计算总页数
    total = Post.objects.count()
    pages = ceil(total / per_page)

    # 取出本页需要现实的文章
    start = (page - 1) * per_page
    end = start + per_page
    posts = Post.objects.all()[start:end]
    return render(request, 'post_list.html', {'posts': posts, 'pages': range(pages)})


def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})
