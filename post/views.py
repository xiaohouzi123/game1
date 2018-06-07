from math import ceil

from django.shortcuts import render, redirect

from post.models import Post
from post.models import Comment
from post.helper import page_cache
from post.helper import read_count
from post.helper import get_top_n
from user.helper import login_required


@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        uid = request.session['uid']
        post = Post.objects.create(uid=uid, title=title, content=content)
        return redirect('/post/read/?post_id=%d' % post.id)
    else:
        return render(request, 'create.html')


@login_required
def edit(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)

        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/post/read/?post_id=%d' % post.id)
    else:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(id=post_id)
        return render(request, 'edit.html', {'post': post})


@read_count
@page_cache(3)
def read(request):
    post_id = int(request.GET.get('post_id'))
    try:
        post = Post.objects.get(id=post_id)  # 取不到的时候，从数据库获取
        return render(request, 'read.html', {'post': post})
    except Post.DoesNotExist:
        return redirect('/')


@page_cache(3)
def post_list(request):
    page = int(request.GET.get('page', 1))  # 当前页码，默认为 1

    per_page = 5
    # 计算总页数
    total = Post.objects.count()
    pages = ceil(total / per_page)

    # 取出本页需要现实的文章
    start = (page - 1) * per_page
    end = start + per_page
    posts = Post.objects.all().order_by('-created')[start:end]
    return render(request, 'post_list.html', {'posts': posts, 'pages': range(pages)})


def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})


def top10(request):
    # rank_data = [
    #     [Post(1), 10],
    #     [Post(3), 9],
    #     [Post(2), 5],
    # ]
    rank_data = get_top_n(10)
    return render(request, 'top10.html', {'rank_data': rank_data})


@login_required
def comment(request):
    uid = request.session['uid']
    post_id = request.POST.get('post_id')
    content = request.POST.get('content')
    Comment.objects.create(uid=uid, post_id=post_id, content=content)
    return redirect('/post/read/?post_id=%s' % post_id)
