# coding: utf-8

import requests
from django.shortcuts import render, redirect
from django.conf import settings

from user.models import User


def weibo_callback(request):
    code = request.GET.get('code')
    # 获取授权的 Access Token
    settings.ACCESS_TOKEN_PARAMS['code'] = code
    resp = requests.post(settings.ACCESS_TOKEN_API, data=settings.ACCESS_TOKEN_PARAMS)
    # 返回值
    # data = {
    #     'access_token': '2.00xnRfUBTRMg7B80794ec7aeGAf_OC',
    #     'remind_in': '157679999',
    #     'expires_in': 157679999,
    #     'uid': '1369262805',
    #     'isRealName': 'true'
    # }
    data1 = resp.json()
    if 'error' in data1:
        return render(request, 'login.html', {'error': data1['error']})

    # 获取微博用户信息
    settings.WEIBO_INFO_PARAMS['access_token'] = data1['access_token']
    settings.WEIBO_INFO_PARAMS['uid'] = data1['uid']
    resp = requests.get(settings.WEIBO_INFO_API, params=settings.WEIBO_INFO_PARAMS)
    data2 = resp.json()
    if 'error' in data2:
        return render(request, 'login.html', {'error': data2['error']})

    # 创建或执行登录
    nickname = data2['screen_name']
    user, _ = User.objects.get_or_create(nickname=nickname, sex='U', age=123)
    request.session['uid'] = user.id
    request.session['nickname'] = user.nickname
    return redirect('/user/info/')
