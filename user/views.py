# coding: utf-8

import logging
from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

from user.models import User
from user.helper import login_required
from user.forms import RegisterForm

info_log = logging.getLogger('inf')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # 创建用户
            user = form.save(commit=False)  # 头像保存，用户创建
            user.password = make_password(user.password)  # 哈希处理密码
            user.save()
            # 记录登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    else:
        return render(request, 'register.html')


def login(request):
    querystring = urlencode(settings.AUTHORIZE_PARAMS)
    weibo_login_api = '%s?%s' % (settings.AUTHORIZE_API, querystring)

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(request, 'login.html',
                          {'error': '用户名错误', 'weibo_login_api': weibo_login_api})
        if check_password(password, user.password):
            # 记录登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            info_log.info('login %s %s' % (user.id, user.nickname))
            return redirect('/user/info/')
        else:
            return render(request, 'login.html',
                          {'error': '密码错误', 'weibo_login_api': weibo_login_api})
    else:
        return render(request, 'login.html', {'weibo_login_api': weibo_login_api})


@login_required
def user_info(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user': user})


@login_required
def logout(request):
    request.session.flush()
    return redirect('/user/login/')
